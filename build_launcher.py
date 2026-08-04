"""
PyInstaller build script for BrightOS Launcher
This script builds a standalone executable launcher that:
- Downloads/updates BrightOS Python files from GitHub
- Installs dependencies
- Runs BrightOS.py
"""
import PyInstaller.__main__
import os
import sys

def build():
    """Build BrightOS Launcher executable using PyInstaller"""
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    launcher_path = os.path.join(script_dir, 'launcher.py')
    icon_path = os.path.join(script_dir, 'docs', 'public', 'favicon.ico')
    
    # Verify files exist
    if not os.path.exists(launcher_path):
        print(f"Error: launcher.py not found at {launcher_path}")
        return 1
    
    if not os.path.exists(icon_path):
        print(f"Warning: favicon.ico not found at {icon_path}, building without icon")
        icon_arg = []
    else:
        icon_arg = [f'--icon={icon_path}']
        print(f"Using icon: {icon_path}")
    
    # PyInstaller arguments
    pyinstaller_args = [
        launcher_path,
        '--name=BrightOS-Launcher',
        '--onefile',
        '--console',  # Keep console for showing installation progress
        '--clean',
        '--noconfirm',
    ] + icon_arg
    
    print("Building BrightOS-Launcher.exe with PyInstaller...")
    print(f"Arguments: {' '.join(pyinstaller_args)}")
    
    try:
        PyInstaller.__main__.run(pyinstaller_args)
        print("\n Build completed successfully!")
        exe_name = 'BrightOS-Launcher.exe' if sys.platform == 'win32' else 'BrightOS-Launcher'
        print(f"Executable location: {os.path.join(script_dir, 'dist', exe_name)}")
        print("\nThe launcher will:")
        print("  1. Download/update BrightOS Python files from GitHub")
        print("  2. Install missing dependencies")
        print("  3. Create necessary directories")
        print("  4. Run BrightOS.py")
        return 0
    except Exception as e:
        print(f"\n Build failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(build())
