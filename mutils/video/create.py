"""
Create a video from an image sequence and perform lossless compression
"""
from pathlib import Path
import argparse
import logging
import itertools
import subprocess

import cv2
import tqdm

def create_video(image_dir, output_path, fps, start_frame, duration_frames, no_compress):
    image_dir = Path(image_dir)

    if output_path:
        output_path = Path(output_path)
    else:
        output_filename = f"{image_dir.name}.mp4"
        output_path = image_dir.parent / output_filename

    if not image_dir.exists():
        logging.error(f"Error: Image directory '{image_dir}' does not exist.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    patterns = ['*.jpg', '*.png', '*.JPG', '*.PNG', '*.jpeg', '*.JPEG']
    all_image_files = sorted(itertools.chain.from_iterable(
        image_dir.glob(pattern) for pattern in patterns
    ), key=lambda x: x.stem)

    logging.info(f"Found {len(all_image_files)} image files in {image_dir}")

    if not all_image_files:
        logging.error("No image files found in the directory.")
        return

    start_idx = start_frame
    if duration_frames == -1:
        end_idx = len(all_image_files)
    else:
        end_idx = min(start_idx + duration_frames, len(all_image_files))

    if start_idx >= len(all_image_files):
        logging.error(f"Error: Start frame {start_idx} exceeds total number of images {len(all_image_files)}.")
        return

    image_files = all_image_files[start_idx:end_idx]
    logging.info(f"Processing frames {start_idx} to {end_idx-1} (total {len(image_files)} frames)")

    first_image = cv2.imread(str(image_files[0]))
    if first_image is None:
        logging.error(f"Cannot read the first image: {image_files[0]}")
        return

    height, width, channels = first_image.shape
    logging.info(f"Video size: {width}x{height}")

    temp_output = output_path.with_suffix('.temp.mp4')

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(str(temp_output), fourcc, fps, (width, height))

    for img_file in tqdm.tqdm(image_files, desc="Creating video"):
        img = cv2.imread(str(img_file))
        if img is None:
            logging.warning(f"Warning: Cannot read image {img_file}")
            continue
        video_writer.write(img)

    video_writer.release()

    logging.info(f"Initial video created: {temp_output}")

    if not no_compress:
        logging.info("Performing lossless compression with ffmpeg...")
        try:
            cmd = [
                'ffmpeg', '-y',
                '-i', str(temp_output),
                '-c:v', 'libx264',
                '-preset', 'slow',
                '-crf', '0',
                str(output_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"Lossless compression completed: {output_path}")
                temp_output.unlink()
            else:
                logging.error(f"ffmpeg compression failed: {result.stderr}")
                logging.info(f"Keeping original video: {temp_output}")
        except FileNotFoundError:
            logging.warning("ffmpeg not found, skipping compression step.")
            logging.info(f"Original video saved as: {temp_output}")
            temp_output.rename(output_path)
    else:
        temp_output.rename(output_path)
        logging.info(f"Video created (not compressed): {output_path}")

    logging.info("\nVideo generation completed!")
    logging.info(f"Output file: {output_path}")
    logging.info(f"Frames processed: {len(image_files)}")
    logging.info(f"Video duration: {len(image_files)/fps:.2f} seconds")

def main():
    parser = argparse.ArgumentParser(description='Create a video from an image sequence and perform lossless compression')
    parser.add_argument('images', help='Directory containing input images')
    parser.add_argument('--out', '-o', type=str, default=None, help='Output video path')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second (default: 30)')
    parser.add_argument('--start_frame', '-s', type=int, default=0, help='Start frame index (default: 0)')
    parser.add_argument('--duration_frames', '-d', type=int, default=-1, 
                       help='Number of frames to process (default: -1, process all)')
    parser.add_argument('--no_compress', action='store_true', 
                       help='Skip lossless compression step')

    args = parser.parse_args()

    create_video(args.images, args.out, args.fps, args.start_frame, args.duration_frames, args.no_compress)

if __name__ == "__main__":
    main() 