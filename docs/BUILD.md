# BrightOS Build and Release Process

This document describes how to build and release BrightOS and its launcher.

## Overview

BrightOS has two components:
1. **BrightOS Python Files** - The main application files that get updated frequently
2. **BrightOS Launcher** - A standalone executable that downloads and runs the Python files

## Release Workflows

### Releasing BrightOS Python Files (Frequent)

The main BrightOS Python files are released automatically when you push a version tag. The launcher will download these files.

#### Creating a BrightOS Release

1. Create and push a version tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. GitHub Actions will:
   - Create a GitHub Release with the tag name
   - Upload `BrightOS.py`, `requirements.txt`, and `build.py` as release assets
   - Users with the launcher will automatically get this update

### Releasing the Launcher (Infrequent)

The launcher executable only needs to be rebuilt when `launcher.py` or `build_launcher.py` changes.

#### Creating a Launcher Release

1. Create and push a launcher version tag:
   ```bash
   git tag launcher-v1.0.0
   git push origin launcher-v1.0.0
   ```

2. GitHub Actions will:
   - Build `BrightOS-Launcher.exe` on Windows (with favicon)
   - Create a GitHub Release with the launcher
   - Upload the executable to the release

#### Manual Launcher Build Trigger

You can also manually trigger a launcher build from the GitHub Actions tab:

1. Go to the Actions tab in your repository
2. Select "Build and Release Launcher" workflow
3. Click "Run workflow"

## Local Builds

### Building BrightOS Executable Locally

If you want to build a standalone BrightOS.exe locally (not recommended for distribution):

#### Prerequisites

- Python 3.11 or later
- Windows operating system (for building .exe files)

#### Steps

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```bash
   python build.py
   ```

3. The executable will be created in the `dist/` folder:
   ```
   dist/BrightOS.exe
   ```

### Building the Launcher Locally

To build the launcher executable yourself:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the launcher build script:
   ```bash
   python build_launcher.py
   ```

3. The executable will be in `dist/BrightOS-Launcher.exe`

## Build Configuration

### BrightOS Build (build.py)

The BrightOS build is configured with these PyInstaller options:

- `--onefile`: Creates a single executable file
- `--windowed`: Runs without a console window (GUI mode)
- `--clean`: Cleans PyInstaller cache before building
- `--noconfirm`: Overwrite output directory without confirmation
- `--icon`: Uses the favicon from `docs/public/favicon.ico`

### Launcher Build (build_launcher.py)

The launcher build uses these PyInstaller options:

- `--onefile`: Creates a single executable file
- `--console`: Shows console for installation progress
- `--clean`: Cleans PyInstaller cache before building
- `--noconfirm`: Overwrite output directory without confirmation
- `--icon`: Uses the favicon from `docs/public/favicon.ico`

## Dependencies

The following Python packages are required (see `requirements.txt`):

- `simple-plugin-loader`: For loading plugins
- `sv-ttk`: For the dark theme UI
- `telemetrix-uno-r4`: For Arduino board communication
- `pyinstaller`: For building executables

## How the System Works

```
┌─────────────────────────┐
│  BrightOS-Launcher.exe  │ ← Users download once
│   (Static executable)   │
└───────────┬─────────────┘
            │
            ├─ Checks GitHub for latest release
            ├─ Downloads BrightOS.py + requirements.txt
            ├─ Installs dependencies
            └─ Runs BrightOS.py
                │
                └─ %USERPROFILE%\AppData\Local\BrightOS\install\
```

**Benefits:**
- Small initial download (just the launcher)
- Auto-updates without re-downloading the .exe
- Python files can be updated frequently
- Launcher rarely needs updates

## Troubleshooting

### Build Fails Locally

- Ensure you're on Windows (for .exe builds)
- Verify Python version is 3.11 or later
- Check that all dependencies are installed: `pip install -r requirements.txt`

### GitHub Actions Build Fails

- Check the Actions tab for error logs
- Verify that the workflow has write permissions for releases
- Ensure the repository has no protected tag rules that prevent the workflow from running

## Directory Structure

```
.
├── BrightOS.py              # Main application
├── launcher.py              # Launcher script
├── build.py                 # Build script for BrightOS.exe
├── build_launcher.py        # Build script for launcher
├── requirements.txt         # Python dependencies
├── docs/
│   └── public/
│       └── favicon.ico      # Icon used for executables
├── .github/
│   └── workflows/
│       ├── build-release.yml    # Release Python files
│       └── build-launcher.yml   # Build launcher executable
├── build/                   # Temporary build files (gitignored)
├── dist/                    # Output directory (gitignored)
└── *.spec                   # PyInstaller spec files (gitignored)
```
