"""
Lazy import utility for avoiding premature module imports
"""

class LazyImporter:
    """
    A lazy importer that delays module import until first use.
    
    This helps avoid circular imports and premature module loading,
    especially useful for package __init__.py files.
    """
    
    def __init__(self, module_name, function_name):
        """
        Initialize the lazy importer.
        
        Args:
            module_name (str): Full module name (e.g., 'mutils.video.sample')
            function_name (str): Function name to import from the module
        """
        self.module_name = module_name
        self.function_name = function_name
        self._function = None
    
    def __getattr__(self, name):
        """Handle attribute access on the lazy imported function."""
        if name == self.function_name and self._function is None:
            # Lazy import the function
            module = __import__(self.module_name, fromlist=[self.function_name])
            self._function = getattr(module, self.function_name)
        return getattr(self._function, name) if self._function else None
    
    def __call__(self, *args, **kwargs):
        """
        Call the lazy imported function.
        
        Args:
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            The result of calling the imported function
        """
        if self._function is None:
            # Lazy import the function
            module = __import__(self.module_name, fromlist=[self.function_name])
            self._function = getattr(module, self.function_name)
        return self._function(*args, **kwargs)
    
    def __repr__(self):
        """String representation of the lazy importer."""
        return f"<LazyImporter: {self.module_name}.{self.function_name}>" 