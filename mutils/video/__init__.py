# lazy import, avoid importing submodules at package initialization
from mutils.utils.lazy_import import LazyImporter

# Create lazy importers for the functions
extract_frames = LazyImporter('mutils.video.sample', 'extract_frames')
create_video = LazyImporter('mutils.video.create', 'create_video')

__all__ = ['extract_frames', 'create_video']