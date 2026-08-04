---
title: "BrightOS v2.0: What's New"
date: 2025-01-13
author: TheCrazy8
tags: [release, features, brightos, v2.0]
excerpt: BrightOS v2.0 brings major improvements including enhanced web interface, example scripts library, and much more. Learn what's new!
---

# BrightOS v2.0: What's New

We're thrilled to announce BrightOS v2.0, packed with new features and improvements based on community feedback!

## 🚀 Major Features

### Enhanced Web Interface

The BrightOS Web Interface has been completely overhauled:

#### Workspace Persistence
Your workspace is now automatically saved to browser localStorage. No more losing your scripts when you close the browser!

- Scripts and plugins persist across sessions
- Automatic save on changes
- Clear workspace option for fresh starts

#### Output Management
Better control over your console output:

- **Copy button** - Copy all output to clipboard with one click
- **Export button** - Download output as `.log` file with timestamp
- **Auto-scroll toggle** - Choose whether output auto-scrolls
- **Clear button** - Clean up your console anytime

#### Example Scripts
Get started faster with 3 preloaded example scripts:

1. **Blink LED** - Classic LED blink demo
2. **Servo Sweep** - Motor control example
3. **Button Input** - Read digital input

### Script Examples Library

A brand new [Examples page](/examples) with comprehensive examples:

**Beginner Level:**
- Blink LED
- Servo Sweep  
- Simple Serial Output

**Intermediate Level:**
- Button Input Handler
- Motor Speed Controller
- Multi-LED Patterns

**Advanced Level:**
- Multi-Sensor Dashboard
- Autonomous Robot Controller

Each example includes:
- Complete, tested code
- Hardware requirements
- Pin configurations
- Expected output
- Safety notes where applicable

### Commit History & Changelog

Stay informed with the new [Changelog page](/changelog):

- Real-time commit history from GitHub API
- Search functionality
- Filter by file type (docs, code, config)
- Grouped by date
- Direct links to GitHub commits
- 5-minute caching to respect API limits

## 🔧 Improvements

### Enhanced Readabilities Plugin

The reading experience is now fully functional with:

- **Spotlight mode** - Focus on specific content
- **Layout switching** - Choose your preferred layout
- **Width adjustments** - Customize content and page width
- **Fully configurable** - Customize to your preferences

### Better Error Handling

More graceful error messages throughout:

- Arduino connection errors displayed clearly
- Script execution errors with helpful context
- API failures with retry options
- Fallback mechanisms for older browsers

### Mobile Responsive

All new features work great on mobile:

- Responsive layouts for all screen sizes
- Touch-friendly controls
- Optimized for mobile browsers
- Reduced clutter on small screens

## 📝 Documentation

### Code Block Copy Buttons

All code blocks now have copy buttons (built into VitePress):
- One-click copy
- Visual feedback
- Works on all code examples

### Navigation Updates

Easier site navigation:
- **Examples** added to nav bar
- **Changelog** added to nav bar
- Updated sidebar organization
- Better discoverability

## 🛠️ Technical Details

### Under the Hood

For developers interested in the technical details:

- Vue 3 Composition API throughout
- localStorage for client-side persistence
- Blob API for file downloads
- GitHub API with caching strategy
- VitePress 1.6.4
- Modern CSS with custom properties

### Plugin System

The plugin system remains compatible:
- All v1.x plugins work with v2.0
- MotorController plugin fully tested
- Telemetrix integration stable
- Easy to create new plugins

## 🎯 What's Next?

We're not stopping here! Coming soon:

- **Blog RSS Feed** - Subscribe to updates
- **Plugin Marketplace** - Enhanced downloads page with search and filters
- **Version Switcher** - Access docs for different versions
- **More Examples** - Additional script examples
- **Video Tutorials** - Visual guides for common tasks

## 📦 Getting v2.0

### Web Interface
Simply visit [BrightOS Web](/brightos-web) - it's already updated!

### Desktop Launcher
Download the latest release:
- [Latest Release](https://github.com/TheCrazy8/Blaze-And-Company-Official/releases/latest)
- [All Releases](https://github.com/TheCrazy8/Blaze-And-Company-Official/releases)

### Building from Source
Follow our [Build Guide](/BUILD) to compile from source.

## 🙏 Thank You

Special thanks to everyone who:
- Reported bugs and issues
- Suggested new features
- Contributed code and documentation
- Tested beta versions
- Shared BrightOS with others

## 🐛 Known Issues

- Python script execution only works in desktop launcher (browser limitation)
- Web Serial API requires Chrome/Edge/Opera (not Firefox or Safari)
- Some mobile browsers may have limited Arduino control

## 💬 Feedback

We'd love to hear your thoughts on v2.0!

- [Open an issue](https://github.com/TheCrazy8/Blaze-And-Company-Official/issues)
- [Start a discussion](https://github.com/TheCrazy8/Blaze-And-Company-Official/discussions)
- Share your projects with the community

Happy coding with BrightOS v2.0! 🎉

---

*Posted by TheCrazy8 on January 13, 2025*
