import argparse
import mutils
import importlib
from pathlib import Path

def get_module_description(module_name):
    """Get the description/docstring of a module."""
    try:
        module = importlib.import_module(module_name)
        if module.__doc__:
            # Get the first non-empty line of the docstring
            lines = [line.strip() for line in module.__doc__.splitlines() if line.strip()]
            if lines:
                return lines[0]
        return "No description available"
    except Exception as e:
        return f"No description available (Error: {str(e)})"

def discover_modules_recursive():
    """Recursively scan the mutils package and its subdirectories to discover all Python modules."""
    modules = []
    def scan_directory(package_path, package_name):
        for item in package_path.iterdir():
            if item.is_dir() and not item.name.startswith('__'):
                # Check if there's an __init__.py file
                init_file = item / '__init__.py'
                if init_file.exists():
                    # This is a Python package, scan recursively
                    scan_directory(item, f"{package_name}.{item.name}")
                else:
                    # Check if there are .py files
                    py_files = list(item.glob('*.py'))
                    if py_files:
                        for py_file in py_files:
                            module_name = f"{package_name}.{item.name}.{py_file.stem}"
                            modules.append(module_name)
            elif item.is_file() and item.suffix == '.py' and item.name != '__init__.py':
                # Direct submodule
                module_name = f"{package_name}.{item.stem}"
                modules.append(module_name)
    # Start scanning from the mutils package root directory
    package_path = Path(mutils.__file__).parent
    scan_directory(package_path, mutils.__name__)
    return modules

def list_functions():
    print("=" * 40)
    print("mutils - Personal Utility Set")
    print("=" * 40)
    print()
    print("Available Functions:\n")
    # Use recursive scanning to discover all modules
    modules = discover_modules_recursive()
    if not modules:
        print("No modules found")
    else:
        # Filter out __main__ module and sort the rest
        filtered_modules = [module for module in modules if not module.endswith('.__main__')]
        for module in sorted(filtered_modules):
            description = get_module_description(module)
            print(f"- {module}: {description}")
            print(f"  View details: python -m {module} --help")
            print()
    print("=" * 40)

def main():
    parser = argparse.ArgumentParser(
        description="mutils - Personal Utility Set",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # no command line arguments, directly call list_functions
    # args = parser.parse_args()
    list_functions()

if __name__ == "__main__":
    main() 