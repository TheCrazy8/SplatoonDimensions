---
title: FAQ
---

# Frequently Asked Questions (FAQ)

[[TOC]]

## General Questions

### What is BrightOS?

BrightOS is an Arduino modular program for managing and running scripts with hardware control capabilities. It provides a cross-platform interface (web and desktop) for controlling Arduino boards, particularly the Arduino Uno R4 WiFi, using the Telemetrix protocol.

### What platforms does BrightOS support?

BrightOS supports:
- **Web Interface**: Works on any modern browser (Chrome, Edge, Opera) with Web Serial API support
- **Desktop**: Windows and Linux via Python launcher
- **Arduino Hardware**: Arduino Uno R4 WiFi board

### Is BrightOS free to use?

Yes! BrightOS is released under the CC BY-NC-SA 4.0 License, which means it's free for non-commercial use.

### How do I get started with BrightOS?

There are three ways to get started:
1. **Web Interface**: Visit the [BrightOS Web Interface](/brightos-web) - no installation required!
2. **Desktop Launcher**: Download the launcher from [releases](https://github.com/TheCrazy8/Blaze-Official/releases) for automated setup
3. **Manual Installation**: Download `BrightOS.py` and install dependencies manually

Check the [Home page](/) for detailed quick start instructions.

## Installation & Setup

### Do I need to install anything to use BrightOS?

Not if you use the web interface! Simply visit the [BrightOS Web Interface](/brightos-web) in a compatible browser. For the desktop version, you'll need Python 3 and the dependencies listed in `requirements.txt`.

### What are the system requirements?

**For Web Interface:**
- Modern web browser (Chrome, Edge, or Opera recommended)
- Web Serial API support (for Arduino connection)

**For Desktop Version:**
- Python 3.7 or higher
- Operating System: Windows, Linux, or macOS
- Internet connection for initial setup

### How do I update BrightOS?

- **Using the Launcher**: Simply run the launcher again - it automatically checks for and downloads updates
- **Manual Installation**: Download the latest release files and replace your existing files

### Where are my plugins and scripts stored?

**Windows:**
```
%USERPROFILE%\AppData\Local\BrightOS\
├── Plugins\
└── Scripts\
```

**Linux/macOS:**
```
~/.brightos/
├── Plugins/
└── Scripts/
```

## Arduino & Hardware

### What Arduino boards are supported?

Currently, BrightOS officially supports the **Arduino Uno R4 WiFi** board through the Telemetrix protocol. Other boards may work but are not officially tested.

### How do I connect my Arduino to BrightOS?

You have three options:

1. **Auto-Discovery (Recommended)**: Use the modified Arduino sketch from `arduino/WiFi_Telemetrix4UnoR4WiFi_AutoDiscovery.ino` - BrightOS will automatically find your Arduino!

2. **Environment Variable**: Set `ARDUINO_IP_ADDRESS` environment variable to your Arduino's IP address

3. **Manual Configuration**: Use the "Configure Telemetrix" button in BrightOS to enter your Arduino's IP address

See the [README](https://github.com/TheCrazy8/Blaze-Official) for detailed setup instructions.

### Do I need special libraries for Arduino?

Yes, you need to install the **Telemetrix4UnoR4** library from the Arduino Library Manager:
1. Open Arduino IDE
2. Go to Sketch → Include Library → Manage Libraries
3. Search for "Telemetrix4UnoR4"
4. Click Install

### My Arduino won't connect. What should I do?

Try these troubleshooting steps:

1. **Check WiFi Connection**: Ensure your Arduino is connected to the same WiFi network as your computer
2. **Verify IP Address**: Open Serial Monitor (115200 baud) to see your Arduino's IP address
3. **Check Firewall**: Make sure your firewall isn't blocking the connection
4. **Use Auto-Discovery Sketch**: Try the auto-discovery sketch from the `arduino/` directory
5. **Check Library**: Ensure Telemetrix4UnoR4 library is properly installed

### Can I use BrightOS without an Arduino?

Yes! You can use BrightOS to run scripts and manage plugins without an Arduino connection. The Arduino connection is only needed for hardware control features.

## Plugins & Scripts

### What's the difference between plugins and scripts?

- **Scripts**: Simple Python files that perform specific tasks
- **Plugins**: More complex modules with additional functionality and integration with BrightOS

Both extend BrightOS's capabilities in different ways.

### How do I install plugins?

1. Visit the [Plugin Marketplace](/downloads)
2. Download the plugin files
3. Place them in your BrightOS Plugins folder:
   - Windows: `%USERPROFILE%\AppData\Local\BrightOS\Plugins\`
   - Linux/macOS: `~/.brightos/Plugins/`
4. Restart BrightOS or reload plugins

### Can I create my own plugins or scripts?

Absolutely! Check out the [Development Guide](/development-guide) for detailed instructions on creating custom plugins and scripts. We also have [examples](/examples) to help you get started.

### Where can I find example scripts?

Visit the [Script Examples](/examples) page for a collection of ready-to-use scripts demonstrating various BrightOS features.

### Can I share my plugins with the community?

Yes! You can share your plugins by:
1. Submitting them to the `community made plugins` directory via GitHub pull request
2. Sharing them on [GitHub Discussions](https://github.com/TheCrazy8/Blaze-Official/discussions)
3. Writing about them in a blog post

## Web Interface

### What browsers support the web interface?

The BrightOS web interface works best on browsers with Web Serial API support:
- ✅ Google Chrome
- ✅ Microsoft Edge
- ✅ Opera
- ❌ Firefox (limited - no Web Serial API support)
- ❌ Safari (limited - no Web Serial API support)

### Can I use the web interface on mobile?

The web interface may work on mobile browsers, but Arduino connection via Web Serial API is not supported on mobile devices. You can still view documentation and examples on mobile.

### Does the web interface work offline?

Yes! The BrightOS website is a Progressive Web App (PWA) with offline support. After your first visit, you can access documentation and some features without an internet connection.

## Development & Contribution

### How can I contribute to BrightOS?

There are many ways to contribute:
- Report bugs or request features via [GitHub Issues](https://github.com/TheCrazy8/Blaze-Official/issues)
- Submit pull requests with improvements
- Share your plugins and scripts
- Help improve documentation
- Participate in [GitHub Discussions](https://github.com/TheCrazy8/Blaze-Official/discussions)

### Is there a developer community?

Yes! Join us on:
- [GitHub Discussions](https://github.com/TheCrazy8/Blaze-Official/discussions)
- [GitHub Repository](https://github.com/TheCrazy8/Blaze-Official)

### How do I report a bug?

Please report bugs on our [GitHub Issues](https://github.com/TheCrazy8/Blaze-Official/issues) page. Include:
- BrightOS version
- Operating system
- Steps to reproduce the issue
- Any error messages
- Expected vs. actual behavior

### Can I request new features?

Absolutely! We welcome feature requests on [GitHub Issues](https://github.com/TheCrazy8/Blaze-Official/issues). Please describe:
- What feature you'd like to see
- Why it would be useful
- How you envision it working

## Competition & Events

### What is the FLARE Competition?

FLARE is a robotics competition hosted by Blaze & Company, similar to VEX and other robotics platforms. Visit the [FLARE Competition](/FLARE%20Competition) page for more information.

### How do I participate in competitions?

Check the [FLARE Competition](/FLARE%20Competition) page for current and upcoming competition information, including registration details and rules.

## Troubleshooting

### I'm getting import errors when running BrightOS

Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

If using the launcher, it should handle this automatically. Try running the launcher again.

### The GUI isn't appearing or looks broken

Try these solutions:
1. Update your Python version to 3.7 or higher
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Check for conflicting GUI libraries

### BrightOS crashes on startup

Common causes and solutions:
1. **Missing dependencies**: Install via `pip install -r requirements.txt`
2. **Outdated Python**: Update to Python 3.7+
3. **Corrupted files**: Redownload BrightOS files
4. **Permissions issue**: Ensure BrightOS has write access to its directories

### Where can I get more help?

If your question isn't answered here:
1. Check the [documentation home page](/)
2. Browse [GitHub Discussions](https://github.com/TheCrazy8/Blaze-Official/discussions)
3. Read the [Development Guide](/development-guide)
4. Open an [issue on GitHub](https://github.com/TheCrazy8/Blaze-Official/issues)
5. Read through the [Blog](/blog/) for tips and updates

## License & Legal

### What license does BrightOS use?

BrightOS is released under the **CC BY-NC-SA 4.0 License** (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International).

### Can I use BrightOS for commercial projects?

The CC BY-NC-SA 4.0 license restricts commercial use. For commercial licensing inquiries, please contact the project maintainers via GitHub.

### Can I modify BrightOS?

Yes! The CC BY-NC-SA 4.0 license allows you to modify BrightOS as long as you:
- Give appropriate credit
- Use the same license for your modifications
- Don't use it for commercial purposes

---

**Still have questions?** Ask them on [GitHub Discussions](https://github.com/TheCrazy8/Blaze-Official/discussions) or check our [Blog](/blog/) for tutorials and updates!
