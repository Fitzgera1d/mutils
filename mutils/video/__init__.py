# lazy import, avoid importing submodules at package initialization
class LazyImporter:
    def __init__(self, module_name, function_name):
        self.module_name = module_name
        self.function_name = function_name
        self._function = None
    
    def __getattr__(self, name):
        if name == self.function_name and self._function is None:
            # lazy import
            module = __import__(self.module_name, fromlist=[self.function_name])
            self._function = getattr(module, self.function_name)
        return getattr(self._function, name) if self._function else None
    
    def __call__(self, *args, **kwargs):
        if self._function is None:
            # lazy import
            module = __import__(self.module_name, fromlist=[self.function_name])
            self._function = getattr(module, self.function_name)
        return self._function(*args, **kwargs)

# Create lazy importers for the functions
extract_frames = LazyImporter('mutils.video.sample', 'extract_frames')
create_video = LazyImporter('mutils.video.create', 'create_video')

__all__ = ['extract_frames', 'create_video']