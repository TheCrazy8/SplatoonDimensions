# Blaze & Company Official

## BrightOS
Arduino modular program for managing and running scripts with hardware control capabilities.

[Launcher Download](https://github.com/TheCrazy8/Blaze-And-Company-Official/releases/tag/launcher-dev-20260113-175555)

### Quick Start

**Option 1: Use the Web Interface (Cross-Platform)**
1. Visit the [BrightOS Web Interface](https://thecrazy8.github.io/Blaze-And-Company-Official/brightos-web) on any modern browser
2. Load your scripts and plugins directly in the browser
3. Connect to Arduino boards using Web Serial API (Chrome/Edge/Opera)
4. No installation required!

**Option 2: Use the Desktop Launcher (Windows/Linux)**
1. **Windows**: Download `BrightOS-Launcher.exe` from the [latest launcher release](https://github.com/TheCrazy8/Blaze-And-Company-Official/releases/tag/launcher-dev-20260113-175555)
2. **Linux**: Download `launcher.py` and run with `python3 launcher.py`
3. The launcher will automatically:
   - Download the latest BrightOS Python files
   - Install dependencies
   - Create necessary directories
   - Launch BrightOS

**Option 3: Run Manually**
1. Download `BrightOS.py` and `requirements.txt` from the [latest release](https://github.com/TheCrazy8/Blaze-And-Company-Official/releases)
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python BrightOS.py`

### Features
- **Cross-Platform Support**: Works on Windows, Linux, and macOS
- **Web Interface**: Run BrightOS directly in your browser with no installation
- Plugin and script loader system
- Telemetrix support for Arduino Uno R4 WiFi board control
- GUI interface with dark theme for running scripts and managing connections
- Arduino Web Serial API support for browser-based control
- Auto-update capability through the desktop launcher
- Custom window icon matching the website

### Directory Structure

When you run BrightOS (via launcher or manually), it creates:

**Windows:**
```
%USERPROFILE%\AppData\Local\BrightOS\
├── install\         # BrightOS files (if using launcher)
├── Plugins\         # Your custom plugins
├── Scripts\         # Your custom scripts
└── Importlist.txt   # Import configuration
```

**Linux/macOS:**
```
~/.brightos/
├── install/         # BrightOS files (if using launcher)
├── Plugins/         # Your custom plugins
├── Scripts/         # Your custom scripts
└── Importlist.txt   # Import configuration
```

### Telemetrix Configuration

#### Arduino Setup

**Option 1: Auto-Discovery Sketch (Recommended)**

Use the modified sketch that automatically broadcasts its IP address:

1. Open Arduino IDE

2. Install Telemetrix4UnoR4 library:
   - Go to Sketch → Include Library → Manage Libraries  
   - Search for "Telemetrix4UnoR4"  
   - Click Install  

3. Load the auto-discovery sketch from this repository:
   - Open `arduino/WiFi_Telemetrix4UnoR4WiFi_AutoDiscovery.ino`
   - See [arduino/README.md](arduino/README.md) for detailed instructions

4. Configure WiFi credentials in `arduino/arduino_secrets.h`:
   ```cpp
   // WiFi credentials for Arduino Uno R4 WiFi  
   #define SECRET_SSID "YOUR_WIFI_NETWORK_NAME"  
   #define SECRET_PASS "YOUR_WIFI_PASSWORD"
   ```

5. Upload to your Arduino Uno R4 WiFi board

6. BrightOS will automatically discover and connect to your Arduino!

**Option 2: Standard Sketch (Manual IP Configuration)**

Use the official sketch if you prefer manual configuration:

1. Open Arduino IDE

2. Install Telemetrix4UnoR4 library (same as above)

3. Load the standard WiFi example:
   - Go to File → Examples → Telemetrix4UnoR4 → WiFi_Telemetrix4UnoR4WiFi  

4. Create `arduino_secrets.h` file in the same folder as the sketch:
   ```cpp
   // WiFi credentials for Arduino Uno R4 WiFi  
   #define SECRET_SSID "YOUR_WIFI_NETWORK_NAME"  
   #define SECRET_PASS "YOUR_WIFI_PASSWORD"
   ```

5. Upload to your Arduino Uno R4 WiFi board

6. Open Serial Monitor (115200 baud) to see the Arduino's IP address:
   ```
   WiFi connected successfully!
   ========================================
   SSID: YourNetworkName  
   IP Address: 192.168.1.xxx
   ========================================
   ```

#### BrightOS Telemetrix Configuration

**Option 1: Automatic Discovery (Recommended)**
1. Use the auto-discovery Arduino sketch (see Arduino Setup Option 1 above)
2. Launch BrightOS - it will automatically discover and connect to your Arduino!
   - No manual configuration needed
   - Works as long as Arduino and computer are on the same network

**Option 2: Environment Variable**
1. Set the `ARDUINO_IP_ADDRESS` environment variable to your Arduino's IP address
2. Launch BrightOS - it will automatically connect to the Arduino board

**Windows:**
```cmd
set ARDUINO_IP_ADDRESS=192.168.1.xxx
python BrightOS.py
```

**Linux/macOS:**
```bash
export ARDUINO_IP_ADDRESS=192.168.1.xxx
python3 BrightOS.py
```

**Option 3: Manual Configuration**
1. Launch BrightOS
2. Click "Configure Telemetrix"
3. Enter your Arduino's IP address
4. Click "Connect"

### Documentation
- [Launcher Documentation](LAUNCHER.md) - Details about the BrightOS Launcher
- [Build Documentation](docs/BUILD.md) - How to build BrightOS and the launcher

### Updates
- **Using the Launcher**: Just run the launcher again - it automatically checks for and downloads updates
- **Manual Installation**: Download the latest release files and replace your existing files
