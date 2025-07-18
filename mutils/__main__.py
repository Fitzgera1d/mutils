import argparse
import mutils
import importlib
import sys
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
    # Define folders and files to ignore
    IGNORE_FOLDERS = {'utils', '__pycache__', '.git', '.vscode', '.idea'}
    IGNORE_FILES = {'__init__.py', '__main__.py', 'setup.py', 'requirements.txt'}
    
    modules = []
    def scan_directory(package_path, package_name):
        for item in package_path.iterdir():
            if item.is_dir() and not item.name.startswith('__'):
                # Skip ignored folders
                if item.name in IGNORE_FOLDERS:
                    continue
                    
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
                            # Skip ignored files
                            if py_file.name in IGNORE_FILES:
                                continue
                            module_name = f"{package_name}.{item.name}.{py_file.stem}"
                            modules.append(module_name)
            elif item.is_file() and item.suffix == '.py' and item.name != '__init__.py':
                # Skip ignored files
                if item.name in IGNORE_FILES:
                    continue
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
            print(f"  View details: mutils {module.replace('mutils.', '')} --help")
            print()
    print("=" * 40)

def run_subcommand(module_name, args):
    """Run a subcommand by importing the module and calling its main function."""
    try:
        # Import the module
        module = importlib.import_module(module_name)
        
        # Check if the module has a main function
        if hasattr(module, 'main'):
            # Set sys.argv to the remaining arguments for the subcommand
            original_argv = sys.argv
            sys.argv = [module_name] + args
            
            try:
                # Call the main function
                module.main()
            finally:
                # Restore original sys.argv
                sys.argv = original_argv
        else:
            print(f"Error: Module {module_name} does not have a main() function")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Error: Could not import module {module_name}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error running {module_name}: {e}")
        sys.exit(1)

def main():
    # 检查是否只有 --help 或 -h 参数，没有子命令
    if len(sys.argv) == 2 and sys.argv[1] in ['--help', '-h']:
        list_functions()
        return
    
    parser = argparse.ArgumentParser(
        description="mutils - Personal Utility Set",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add subcommand argument
    parser.add_argument('subcommand', nargs='?', help='Subcommand to run (e.g., video.sample)')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments for the subcommand')
    
    args = parser.parse_args()
    
    if args.subcommand is None:
        # No subcommand provided, show available functions
        list_functions()
    else:
        # Construct the full module name
        module_name = f"mutils.{args.subcommand}"
        
        # Run the subcommand
        run_subcommand(module_name, args.args)

if __name__ == "__main__":
    main() 