"""
PyInstaller build script for BrightOS.py
This script builds a standalone executable for BrightOS
"""
import PyInstaller.__main__
import os
import sys

def build():
    """Build BrightOS.exe using PyInstaller"""
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    brightos_path = os.path.join(script_dir, 'BrightOS.py')
    icon_path = os.path.join(script_dir, 'docs', 'public', 'favicon.ico')
    
    # Check if icon exists
    if not os.path.exists(icon_path):
        print(f"Warning: favicon.ico not found at {icon_path}, building without icon")
        icon_arg = []
    else:
        icon_arg = [f'--icon={icon_path}']
        print(f"Using icon: {icon_path}")
    
    # PyInstaller arguments
    pyinstaller_args = [
        brightos_path,
        '--name=BrightOS',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
    ] + icon_arg
    
    print("Building BrightOS.exe with PyInstaller...")
    print(f"Arguments: {' '.join(pyinstaller_args)}")
    
    try:
        PyInstaller.__main__.run(pyinstaller_args)
        print("\n Build completed successfully!")
        print(f"Executable location: {os.path.join(script_dir, 'dist', 'BrightOS.exe')}")
        return 0
    except Exception as e:
        print(f"\n Build failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(build())
