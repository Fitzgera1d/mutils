"""
Extract evenly sampled frames from video
"""
from pathlib import Path
import argparse
import logging

import cv2

def extract_frames(video_path, num_frames, output_dir, prefix="frame_", suffix="jpg", pad0=6):
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Open video file
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        logging.error(f"Cannot open video file: {video_path}")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        logging.error("Video has 0 frames, cannot process.")
        return

    # Calculate sampling interval
    interval = max(total_frames // num_frames, 1)
    selected_indices = [i * interval for i in range(num_frames)]
    selected_indices = [min(idx, total_frames - 1) for idx in selected_indices]

    frame_id = 0
    saved = 0
    while cap.isOpened() and saved < num_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_id in selected_indices:
            out_path = output_path / f"{prefix}{saved:0{pad0}d}.{suffix}"
            cv2.imwrite(str(out_path), frame)
            saved += 1
        frame_id += 1
    cap.release()
    logging.info(f"Saved {saved} frames to {output_dir}")


def main():    
    parser = argparse.ArgumentParser(description="Extract evenly sampled frames from video")
    parser.add_argument('video', type=str, help='Input video path')
    parser.add_argument('--num', '-n', type=int, required=True, help='Number of frames to extract')
    parser.add_argument('--out', '-o', type=str, required=True, help='Output directory')
    parser.add_argument('--prefix', type=str, default='frame_', help='Frame filename prefix (default: frame_)')
    parser.add_argument('--suffix', type=str, default='jpg', help='Frame filename suffix (default: jpg)')
    parser.add_argument('--pad0', type=int, default=6, help='Number of zeros to pad frame numbers (default: 6)')
    args = parser.parse_args()
    
    extract_frames(args.video, args.num, args.out, args.prefix, args.suffix, args.pad0)

if __name__ == "__main__":
    main()