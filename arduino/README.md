# Arduino WiFi Telemetrix with Auto-Discovery

This directory contains a modified version of the official WiFi Telemetrix sketch that adds automatic IP address broadcasting for network discovery.

## What's Different?

This sketch extends the standard `WiFi_Telemetrix4UnoR4WiFi` example with:
- **UDP broadcast functionality** that periodically announces the Arduino's IP address
- **Automatic discovery** by BrightOS without manual IP configuration
- **Multicast support** for better network compatibility

## Files

- `WiFi_Telemetrix4UnoR4WiFi_AutoDiscovery.ino` - Main Arduino sketch with auto-discovery
- `arduino_secrets.h` - WiFi credentials (you need to fill this in)

## Setup Instructions

### 1. Install Required Library

In Arduino IDE:
1. Go to **Sketch → Include Library → Manage Libraries**
2. Search for **"Telemetrix4UnoR4"**
3. Click **Install**

### 2. Configure WiFi Credentials

1. Copy `arduino_secrets.h.template` to `arduino_secrets.h`:
   ```bash
   # In the arduino directory
   cp arduino_secrets.h.template arduino_secrets.h
   ```

2. Edit `arduino_secrets.h` and replace with your WiFi network details:

```cpp
#define SECRET_SSID "YOUR_WIFI_NETWORK_NAME"
#define SECRET_PASS "YOUR_WIFI_PASSWORD"
```

### 3. Upload to Arduino

1. Connect your Arduino Uno R4 WiFi board
2. Open `WiFi_Telemetrix4UnoR4WiFi_AutoDiscovery.ino` in Arduino IDE
3. Select your board: **Tools → Board → Arduino Uno R4 WiFi**
4. Select your port: **Tools → Port → (select your Arduino)**
5. Click **Upload**

### 4. Verify Operation

Open Serial Monitor (115200 baud) and you should see:

```
Starting WiFi Telemetrix with Auto-Discovery...
Connecting to WiFi network: YourNetworkName
WiFi connected successfully!
========================================
SSID: YourNetworkName
IP Address: 192.168.1.xxx
Signal strength (RSSI): -45 dBm
========================================
Setup complete!
Broadcasting IP address for auto-discovery...
```

## How It Works

The Arduino broadcasts its IP address every 5 seconds using UDP:
- **Broadcast IP**: 255.255.255.255
- **Multicast IP**: 239.255.255.250
- **Port**: 48879
- **Message format**: `BRIGHTOS_ARDUINO:192.168.1.xxx`

BrightOS listens on port 48879 for these broadcasts and automatically connects when an Arduino is discovered.

## Troubleshooting

**Arduino doesn't connect to WiFi:**
- Double-check your WiFi credentials in `arduino_secrets.h`
- Make sure your network uses 2.4GHz (Arduino Uno R4 WiFi doesn't support 5GHz)
- Check if your network has client isolation disabled

**BrightOS doesn't discover Arduino:**
- Make sure both devices are on the same network
- Check if your router allows UDP broadcasts (some routers block this)
- Verify the Arduino is running (check Serial Monitor)
- Try setting the IP manually using the environment variable: `export ARDUINO_IP_ADDRESS=192.168.1.xxx`

**Connection is unstable:**
- Move Arduino closer to your WiFi router
- Check signal strength in Serial Monitor (should be above -70 dBm)
- Ensure your computer's firewall allows UDP traffic on port 48879

## Comparison with Standard Sketch

| Feature | Standard WiFi Sketch | Auto-Discovery Sketch |
|---------|---------------------|----------------------|
| Telemetrix protocol | ✅ Yes | ✅ Yes |
| WiFi connectivity | ✅ Yes | ✅ Yes |
| IP broadcast | ❌ No | ✅ Yes |
| Auto-discovery | ❌ No | ✅ Yes |
| Manual IP config | ✅ Required | ⚠️ Optional fallback |

## Network Requirements

- Arduino and computer must be on the same local network
- Router must allow UDP broadcasts (most home routers do)
- No client isolation enabled
- Firewall must allow UDP port 48879

## Security Note

This sketch broadcasts the Arduino's IP address on your local network. This is generally safe for home networks, but be aware that any device on the same network can see the broadcast. For sensitive environments, use the manual IP configuration method instead.
