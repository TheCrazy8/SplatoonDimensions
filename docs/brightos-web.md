---
title: BrightOS Web Interface
---

# BrightOS Web Interface

Run BrightOS directly in your browser! This web interface allows you to load plugins and scripts, and control Arduino boards using the Web Serial API.

<script setup>
import BrightOSWeb from './.vitepress/theme/components/BrightOSWeb.vue'
</script>

<BrightOSWeb />

## Features

- **Plugin Loader**: Load and manage BrightOS plugins directly in your browser
- **Script Runner**: Execute custom scripts with real-time output
- **Arduino Control**: Connect to Arduino boards via Web Serial API (Chrome/Edge only)
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Requirements

- Modern web browser (Chrome, Edge, or Opera recommended for Arduino support)
- USB connection for Arduino control (requires HTTPS or localhost)

## How to Use

### Loading Scripts

1. Click "Load Script" to upload a Python script file
2. The script will be parsed and made available in the dropdown
3. Select your script and click "Run" to execute it

### Connecting to Arduino

1. Click "Connect Arduino" button
2. Select your Arduino from the serial port list
3. Once connected, scripts can communicate with the board

::: tip Web Serial API Support
Arduino control via Web Serial API is currently supported in Chrome, Edge, and Opera browsers. Firefox and Safari do not yet support this feature.
:::

## Security Note

Scripts are executed in a sandboxed environment for security. Only load scripts from trusted sources.
