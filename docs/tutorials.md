---
title: Tutorials
---

# Tutorials

Step-by-step guides to help you get the most out of BrightOS.

[[TOC]]

## Getting Started Tutorials

### Tutorial 1: Your First BrightOS Experience (Web)

**Difficulty:** Beginner | **Time:** 10 minutes

Learn how to use BrightOS in your browser without installing anything.

#### What You'll Learn
- How to access the web interface
- Running a simple script
- Understanding the BrightOS interface

#### Steps

1. **Open the Web Interface**
   - Visit the [BrightOS Web Interface](/brightos-web)
   - The interface should load in your browser

2. **Explore the Interface**
   - Look at the main window with dark theme
   - Notice the menu bar at the top
   - Check the status bar at the bottom

3. **Load a Sample Script**
   - Click on "Scripts" menu
   - Select a sample script from the list
   - Read the script description

4. **Run Your First Script**
   - Click the "Run" button
   - Observe the output in the console
   - Check the status messages

::: tip Success!
You've successfully run your first BrightOS script in the browser! 🎉
:::

---

### Tutorial 2: Installing BrightOS Desktop

**Difficulty:** Beginner | **Time:** 15 minutes

Set up BrightOS on your Windows or Linux computer.

#### What You'll Learn
- How to download the launcher
- Installing dependencies automatically
- Running BrightOS for the first time

#### Requirements
- Windows 10+ or Linux
- Internet connection
- Python 3.7+ (will be checked automatically)

#### Steps for Windows

1. **Download the Launcher**
   - Go to the [releases page](https://github.com/TheCrazy8/Blaze-Official/releases)
   - Find the latest launcher release (look for tags starting with "launcher-")
   - Download `BrightOS-Launcher.exe`
   - Save it to a folder you can easily access

2. **Run the Launcher**
   - Double-click `BrightOS-Launcher.exe`
   - Windows SmartScreen might appear - click "More info" → "Run anyway"
   - The launcher will automatically:
     - Check for Python installation
     - Download BrightOS files
     - Install dependencies
     - Create necessary directories

3. **First Launch**
   - Wait for the launcher to complete setup
   - BrightOS window will open automatically
   - You'll see the main GUI with dark theme

#### Steps for Linux

1. **Download the Launcher**
   - Go to the [releases page](https://github.com/TheCrazy8/Blaze-Official/releases)
   - Find the latest launcher release (look for tags starting with "launcher-")
   - Download `launcher.py`

2. **Make it Executable (Optional)**
   ```bash
   chmod +x launcher.py
   ```

3. **Run the Launcher**
   ```bash
   python3 launcher.py
   ```
   - The launcher will automatically handle setup
   - BrightOS will launch when ready

::: tip Pro Tip
The launcher automatically checks for updates every time you run it!
:::

---

### Tutorial 3: Manual Installation

**Difficulty:** Intermediate | **Time:** 10 minutes

Install BrightOS manually for more control over the setup.

#### What You'll Learn
- Manual installation process
- Dependency management
- Directory structure

#### Requirements
- Python 3.7 or higher
- pip (Python package manager)
- Git (optional)

#### Steps

1. **Download BrightOS Files**
   
   Option A - Using Git:
   ```bash
   git clone https://github.com/TheCrazy8/Blaze-Official.git
   cd Blaze-Official
   ```
   
   Option B - Manual Download:
   - Go to the [releases page](https://github.com/TheCrazy8/Blaze-Official/releases)
   - Find the latest BrightOS release
   - Download `BrightOS.py` and `requirements.txt`
   - Save to a folder

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create Directories**
   
   Windows:
   ```cmd
   mkdir "%USERPROFILE%\AppData\Local\BrightOS\Plugins"
   mkdir "%USERPROFILE%\AppData\Local\BrightOS\Scripts"
   ```
   
   Linux/macOS:
   ```bash
   mkdir -p ~/.brightos/Plugins
   mkdir -p ~/.brightos/Scripts
   ```

4. **Run BrightOS**
   ```bash
   python3 BrightOS.py
   ```

::: warning Note
With manual installation, you'll need to manually check for updates by downloading new releases.
:::

---

## Arduino Setup Tutorials

### Tutorial 4: Setting Up Arduino Uno R4 WiFi

**Difficulty:** Intermediate | **Time:** 30 minutes

Connect your Arduino Uno R4 WiFi board to BrightOS.

#### What You'll Need
- Arduino Uno R4 WiFi board
- USB cable
- Arduino IDE installed
- WiFi network

#### Steps

1. **Install Arduino IDE**
   - Download from [arduino.cc](https://www.arduino.cc/en/software)
   - Install following the platform-specific instructions

2. **Install Telemetrix4UnoR4 Library**
   - Open Arduino IDE
   - Go to **Sketch** → **Include Library** → **Manage Libraries**
   - Search for "Telemetrix4UnoR4"
   - Click **Install**
   - Wait for installation to complete

3. **Create WiFi Credentials File**
   - In Arduino IDE, create a new tab: **File** → **New Tab**
   - Name it `arduino_secrets.h`
   - Add the following code:
   ```cpp
   // WiFi credentials for Arduino Uno R4 WiFi
   #define SECRET_SSID "Your_WiFi_Network_Name"
   #define SECRET_PASS "Your_WiFi_Password"
   ```
   - Replace with your actual WiFi credentials
   - Save the file
   
   ::: warning Security Note
   Never commit WiFi credentials to version control! Keep `arduino_secrets.h` in your `.gitignore` file if sharing your project publicly.
   :::

4. **Load the Auto-Discovery Sketch**
   - Clone or download the Blaze repository
   - Open `arduino/WiFi_Telemetrix4UnoR4WiFi_AutoDiscovery.ino`
   - Verify the code compiles (checkmark button)

5. **Upload to Arduino**
   - Connect Arduino via USB
   - Select the correct board: **Tools** → **Board** → **Arduino Uno R4 WiFi**
   - Select the correct port: **Tools** → **Port**
   - Click **Upload** (arrow button)
   - Wait for "Done uploading" message

6. **Verify Connection**
   - Open Serial Monitor: **Tools** → **Serial Monitor**
   - Set baud rate to **115200**
   - You should see:
   ```
   WiFi connected successfully!
   ========================================
   SSID: YourNetworkName
   IP Address: 192.168.1.xxx
   ========================================
   ```

::: tip Success!
Your Arduino is now ready to work with BrightOS! The auto-discovery feature means BrightOS will automatically find it.
:::

---

### Tutorial 5: Connecting Arduino to BrightOS

**Difficulty:** Beginner | **Time:** 5 minutes

Connect your configured Arduino to BrightOS.

#### Prerequisites
- Arduino Uno R4 WiFi configured (Tutorial 4)
- BrightOS installed (Tutorial 2 or 3)
- Both on the same WiFi network

#### Method 1: Auto-Discovery (Recommended)

1. **Start Arduino**
   - Power on your Arduino (USB or external power)
   - Wait for it to connect to WiFi (usually 5-10 seconds)

2. **Launch BrightOS**
   - Run BrightOS launcher or `python3 BrightOS.py`
   - BrightOS will automatically search for your Arduino
   - Look for "Arduino discovered" message

3. **Verify Connection**
   - Check the status bar for "Connected to Arduino"
   - Green indicator shows successful connection

#### Method 2: Manual Configuration

1. **Get Arduino IP Address**
   - Open Arduino Serial Monitor
   - Note the IP address displayed

2. **Configure BrightOS**
   - Launch BrightOS
   - Click **"Configure Telemetrix"**
   - Enter Arduino IP address: `192.168.1.xxx`
   - Click **"Connect"**

3. **Save Configuration**
   - BrightOS will remember this IP for next time
   - Or set environment variable `ARDUINO_IP_ADDRESS`

::: tip Troubleshooting
If connection fails:
- Ensure both devices are on the same network
- Check firewall settings
- Verify Arduino IP hasn't changed (use DHCP reservation)
- Restart both devices
:::

---

## Plugin Development Tutorials

### Tutorial 6: Creating Your First Plugin

**Difficulty:** Intermediate | **Time:** 45 minutes

Create a custom BrightOS plugin to extend functionality.

#### What You'll Learn
- Plugin structure
- BrightOS API basics
- Loading and testing plugins

#### Prerequisites
- BrightOS installed
- Basic Python knowledge
- Text editor or IDE

#### Steps

1. **Create Plugin Directory**
   - Navigate to your Plugins folder:
     - Windows: `%USERPROFILE%\AppData\Local\BrightOS\Plugins\`
     - Linux/macOS: `~/.brightos/Plugins/`
   - Create a new folder: `my_first_plugin`

2. **Create Plugin File**
   - Inside `my_first_plugin`, create `__init__.py`
   - Add the following code:
   
   ```python
   """
   My First Plugin
   A simple plugin that greets the user
   """
   
   class MyFirstPlugin:
       def __init__(self):
           self.name = "My First Plugin"
           self.version = "1.0.0"
           self.description = "A simple greeting plugin"
       
       def initialize(self):
           """Called when plugin is loaded"""
           print(f"{self.name} v{self.version} initialized!")
       
       def greet(self, name="User"):
           """Greet the user"""
           return f"Hello, {name}! Welcome to BrightOS!"
       
       def get_info(self):
           """Return plugin information"""
           return {
               "name": self.name,
               "version": self.version,
               "description": self.description
           }
   
   # Plugin entry point
   def load_plugin():
       return MyFirstPlugin()
   ```

3. **Test Your Plugin**
   - Restart BrightOS
   - Check the console for initialization message
   - Your plugin should appear in the plugins list

4. **Use Your Plugin**
   - Access from BrightOS scripts:
   ```python
   plugin = get_plugin("My First Plugin")
   message = plugin.greet("Alice")
   print(message)  # Output: Hello, Alice! Welcome to BrightOS!
   ```

::: tip Next Steps
Expand your plugin with:
- Arduino hardware control
- File operations
- User interface elements
- Configuration options
:::

See the [Development Guide](/development-guide) for more advanced plugin features.

---

### Tutorial 7: Creating a Simple Script

**Difficulty:** Beginner | **Time:** 20 minutes

Write a simple BrightOS script.

#### What You'll Learn
- Script structure
- Using BrightOS functions
- Saving and running scripts

#### Steps

1. **Create Script File**
   - Navigate to Scripts folder:
     - Windows: `%USERPROFILE%\AppData\Local\BrightOS\Scripts\`
     - Linux/macOS: `~/.brightos/Scripts/`
   - Create `hello_world.py`

2. **Write Script Code**
   ```python
   """
   Hello World Script
   Description: A simple script that prints a greeting
   Author: Your Name
   Version: 1.0
   """
   
   def main():
       print("="*50)
       print("Hello from BrightOS!")
       print("This is my first custom script.")
       print("="*50)
       
       # Get user input
       name = input("What's your name? ")
       print(f"\nNice to meet you, {name}!")
       print(f"Welcome to the BrightOS community!")
   
   if __name__ == "__main__":
       main()
   ```

3. **Run Your Script**
   - Open BrightOS
   - Go to Scripts menu
   - Select "hello_world"
   - Click Run

4. **Enhance Your Script**
   Add Arduino interaction:
   ```python
   def blink_led(board, pin=13, times=3):
       """Blink an LED on the Arduino"""
       import time
       
       board.set_pin_mode_digital_output(pin)
       
       for i in range(times):
           board.digital_write(pin, 1)
           time.sleep(0.5)
           board.digital_write(pin, 0)
           time.sleep(0.5)
       
       print(f"Blinked LED {times} times!")
   ```

::: tip Pro Tip
Check out the [Examples page](/examples) for more script ideas and templates!
:::

---

## Advanced Tutorials (Coming Soon)

::: info Under Development
The following advanced tutorials are currently being developed. Check back soon or subscribe to the [RSS Feed](/blog/feed.xml) for updates when they're published!
:::

### Tutorial 8: Using Arduino Sensors

**Difficulty:** Advanced | **Time:** 60 minutes | **Status:** 🚧 In Development

Learn how to read sensor data from Arduino using BrightOS.

#### What You'll Need
- Arduino Uno R4 WiFi configured
- Temperature sensor (e.g., DHT11, DHT22)
- Breadboard and wires

Check the [Examples page](/examples) for sensor examples while this tutorial is being completed.

---

### Tutorial 9: Creating a Dashboard Plugin

**Difficulty:** Advanced | **Time:** 90 minutes | **Status:** 🚧 In Development

Build a custom dashboard plugin with real-time data visualization.

Check the [Development Guide](/development-guide) for UI plugin examples while this tutorial is being completed.

---

## Video Tutorials

::: info Coming Soon
Video tutorials are in production. Subscribe to the [RSS Feed](/blog/feed.xml) to be notified when they're available!
:::

---

## Need More Help?

- Check the [FAQ](/faq) for common questions
- Browse [Examples](/examples) for code samples
- Read the [Development Guide](/development-guide)
- Ask questions on [GitHub Discussions](https://github.com/TheCrazy8/Blaze-Official/discussions)
- Report issues on [GitHub Issues](https://github.com/TheCrazy8/Blaze-Official/issues)

---

## Tutorial Requests

Have an idea for a tutorial? [Request it on GitHub Discussions](https://github.com/TheCrazy8/Blaze-Official/discussions) or [open an issue](https://github.com/TheCrazy8/Blaze-Official/issues) with the "documentation" label.

**Popular requests:**
- Working with motors and servos
- Creating custom GUI interfaces
- Multi-Arduino setups
- Advanced Telemetrix features
- Plugin best practices

Check back regularly for new tutorials!
