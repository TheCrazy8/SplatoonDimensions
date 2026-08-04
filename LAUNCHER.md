# BrightOS Launcher

The BrightOS Launcher is a cross-platform tool that automatically manages your BrightOS installation.

## What it does

The launcher:
1. **Downloads/Updates BrightOS** - Automatically fetches the latest Python files from GitHub
2. **Installs Dependencies** - Ensures all required Python packages are installed
3. **Creates Directories** - Sets up all necessary folders for BrightOS
4. **Runs BrightOS** - Launches the BrightOS application

## Usage

### Windows
Simply run `BrightOS-Launcher.exe` and it will:
- Check for updates to the BrightOS Python files
- Download any updates if available
- Install any missing dependencies
- Launch BrightOS

### Linux/macOS
Run the launcher with Python:
```bash
python3 launcher.py
```

Or make it executable:
```bash
chmod +x launcher.py
./launcher.py
```

The launcher will perform the same automatic setup and launch process.

## Directory Structure

The launcher creates the following directory structure:

### Windows
```
%USERPROFILE%\AppData\Local\BrightOS\
├── install\           # BrightOS Python files
│   ├── BrightOS.py
│   ├── requirements.txt
│   └── version.txt
├── Plugins\           # User plugins
├── Scripts\           # User scripts
└── Importlist.txt     # Import configuration
```

### Linux/macOS
```
~/.brightos/
├── install/           # BrightOS Python files
├── Plugins/           # User plugins
├── Scripts/           # User scripts
└── Importlist.txt     # Import configuration
```

## Building the Launcher

To build the launcher executable yourself:

### Windows
1. Install dependencies:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python build_launcher.py
   ```

3. The executable will be in `dist/BrightOS-Launcher.exe`

### Linux/macOS
1. Install dependencies:
   ```bash
   pip3 install pyinstaller
   ```

2. Run the build script:
   ```bash
   python3 build_launcher.py
   ```

3. The executable will be in `dist/BrightOS-Launcher`

You can also run the launcher directly with Python without building:
```bash
python3 launcher.py
```

## How Updates Work

- The **launcher** (`.exe` on Windows or `.py` script) is a tool you run locally
- When you run it, it automatically downloads the latest **Python files** from GitHub releases
- The launcher first tries to download individual files from release assets (faster and more efficient)
- If release assets aren't available, it falls back to downloading the full repository zip
- You don't need to download a new launcher for BrightOS updates - just run it again
- Updates are pulled from the GitHub repository's latest release or main branch
- **Cross-platform**: Works on Windows, Linux, and macOS

## Advantages

- **Cross-platform** - Works on Windows, Linux, and macOS
- **Small download size** - The launcher is lightweight
- **Auto-updates** - Always get the latest BrightOS features automatically
- **Flexible** - Use the compiled executable on Windows or run the Python script directly
- **Easy to use** - Just run and go
