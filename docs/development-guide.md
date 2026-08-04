# Creating Plugins and Scripts for BrightOS

Learn how to create your own plugins and scripts to extend BrightOS functionality.

## Table of Contents
- [Understanding the Difference](#understanding-the-difference)
- [Creating Plugins](#creating-plugins)
- [Creating Scripts](#creating-scripts)
- [Best Practices](#best-practices)
- [Testing Your Code](#testing-your-code)
- [Sharing Your Work](#sharing-your-work)

---

## Understanding the Difference

### What is a Plugin?

A **plugin** is a reusable Python class that provides functionality to multiple scripts. Think of plugins as libraries or tools that scripts can use.

**Example use cases:**
- Motor controller (servo, DC motor control)
- Sensor reader (temperature, distance, etc.)
- Display controller (LED matrix, LCD)
- Data logger
- Math utilities

### What is a Script?

A **script** is a Python program that accomplishes a specific task. Scripts use plugins and the telemetrix board to interact with hardware.

**Example use cases:**
- Robot movement sequence
- Environmental monitoring
- Light show
- Game controller
- Automated testing

**Key Difference:** Plugins are **tools**, scripts are **programs** that use those tools.

---

## Creating Plugins

### Basic Plugin Structure

Every plugin must inherit from `SamplePlugin`:

```python
from simple_plugin_loader.sample_plugin import SamplePlugin

class MyPlugin(SamplePlugin):
    """
    Brief description of what your plugin does.
    """
    
    def __init__(self):
        """Initialize your plugin"""
        self._board = None
        # Initialize other variables here
    
    def set_board(self, board):
        """
        Set the telemetrix board instance.
        
        Args:
            board: TelemetrixUnoR4WiFi board instance
        """
        self._board = board
    
    def my_function(self, param1, param2):
        """
        Description of what this function does.
        
        Args:
            param1: Description of first parameter
            param2: Description of second parameter
            
        Returns:
            Description of return value
        """
        if not self._board:
            self.eprint("Board not connected")
            return False
        
        # Your code here
        self.print(f"Doing something with {param1} and {param2}")
        return True
```

### Plugin Methods Explained

#### Inherited from SamplePlugin

- `self.print(message)` - Print a message with your plugin name prefix
- `self.eprint(message)` - Print an error message to stderr
- `self.plugin_name` - Get your plugin's class name

#### Custom Methods

You can add any methods you need. Common patterns:

```python
# Initialization/setup
def set_board(self, board):
    self._board = board

# Configuration
def configure(self, option1, option2):
    self._config = {"option1": option1, "option2": option2}

# Core functionality
def do_something(self, param):
    # Your logic here
    pass

# Cleanup
def cleanup(self):
    # Stop operations, release resources
    pass
```

### Complete Plugin Example

Here's a complete example of a LED controller plugin:

```python
from simple_plugin_loader.sample_plugin import SamplePlugin
import time

class LEDController(SamplePlugin):
    """
    Plugin for controlling LEDs connected to Arduino pins.
    Supports on/off, blinking, and fading.
    """
    
    def __init__(self):
        self._board = None
        self._led_pins = {}  # Track configured LED pins
    
    def set_board(self, board):
        """Set the telemetrix board instance"""
        self._board = board
    
    def setup_led(self, pin, pwm=False):
        """
        Configure a pin for LED control.
        
        Args:
            pin (int): Arduino pin number
            pwm (bool): Use PWM for brightness control (default: False)
            
        Returns:
            bool: True if successful
        """
        if not self._board:
            self.eprint("Board not connected")
            return False
        
        try:
            if pwm:
                self._board.set_pin_mode_analog_output(pin)
            else:
                self._board.set_pin_mode_digital_output(pin)
            
            self._led_pins[pin] = {"pwm": pwm, "state": 0}
            self.print(f"LED configured on pin {pin} (PWM: {pwm})")
            return True
            
        except Exception as e:
            self.eprint(f"Error setting up LED on pin {pin}: {e}")
            return False
    
    def turn_on(self, pin, brightness=100):
        """
        Turn on an LED.
        
        Args:
            pin (int): Arduino pin number
            brightness (int): Brightness 0-100 (only for PWM pins)
            
        Returns:
            bool: True if successful
        """
        if not self._board or pin not in self._led_pins:
            self.eprint(f"LED on pin {pin} not configured")
            return False
        
        try:
            if self._led_pins[pin]["pwm"]:
                value = int((brightness / 100.0) * 255)
                self._board.analog_write(pin, value)
            else:
                self._board.digital_write(pin, 1)
            
            self._led_pins[pin]["state"] = brightness
            self.print(f"LED on pin {pin} turned on")
            return True
            
        except Exception as e:
            self.eprint(f"Error turning on LED: {e}")
            return False
    
    def turn_off(self, pin):
        """Turn off an LED"""
        if not self._board or pin not in self._led_pins:
            return False
        
        try:
            if self._led_pins[pin]["pwm"]:
                self._board.analog_write(pin, 0)
            else:
                self._board.digital_write(pin, 0)
            
            self._led_pins[pin]["state"] = 0
            self.print(f"LED on pin {pin} turned off")
            return True
            
        except Exception as e:
            self.eprint(f"Error turning off LED: {e}")
            return False
    
    def blink(self, pin, times=3, interval=0.5):
        """
        Blink an LED multiple times.
        
        Args:
            pin (int): Arduino pin number
            times (int): Number of blinks
            interval (float): Seconds between blinks
        """
        for _ in range(times):
            self.turn_on(pin)
            time.sleep(interval)
            self.turn_off(pin)
            time.sleep(interval)
    
    def fade(self, pin, start=0, end=100, steps=50, delay=0.02):
        """
        Fade an LED from start to end brightness.
        Only works with PWM pins.
        
        Args:
            pin (int): Arduino pin number (must be PWM)
            start (int): Starting brightness 0-100
            end (int): Ending brightness 0-100
            steps (int): Number of steps in fade
            delay (float): Delay between steps in seconds
        """
        if pin not in self._led_pins or not self._led_pins[pin]["pwm"]:
            self.eprint(f"Pin {pin} not configured for PWM")
            return False
        
        step_size = (end - start) / steps
        for i in range(steps + 1):
            brightness = int(start + (step_size * i))
            self.turn_on(pin, brightness)
            time.sleep(delay)
        
        return True
    
    def cleanup(self):
        """Turn off all LEDs"""
        for pin in list(self._led_pins.keys()):
            self.turn_off(pin)
        self.print("All LEDs turned off")
```

### Saving Your Plugin

1. Save your plugin file with a descriptive name: `my_plugin.py`
2. Copy it to the BrightOS Plugins directory:
   - **Windows**: `%USERPROFILE%\AppData\Local\BrightOS\Plugins\`
   - **Linux/macOS**: `~/.brightos/Plugins/`
3. Restart BrightOS

---

## Creating Scripts

### Basic Script Structure

Every script needs a `main()` function and optionally a `stop()` function:

```python
def main(plugins):
    """
    Main function - executed when script runs.
    
    Args:
        plugins: Dictionary of loaded plugins including 'telemetrix'
    """
    # Get the telemetrix board
    board = plugins.get("telemetrix")
    
    if not board:
        print("ERROR: Telemetrix board not connected")
        return
    
    print("Script starting...")
    
    # Your script code here
    
    print("Script completed")


def stop():
    """
    Optional: Called when user clicks Stop button.
    Use this to clean up and stop operations.
    """
    print("Stop requested - cleaning up...")
    # Stop motors, turn off LEDs, etc.
```

### Accessing Plugins in Scripts

Plugins are accessed through the `plugins` dictionary using lowercase keys:

```python
def main(plugins):
    # Get the telemetrix board
    board = plugins.get("telemetrix")
    
    # Get custom plugins (keys are lowercase)
    motor = plugins.get("motorcontroller")
    led = plugins.get("ledcontroller")
    sensor = plugins.get("sensormanager")
    
    # Initialize plugins with the board
    if motor and board:
        motor.set_board(board)
        motor.servo_control(9, 90)
    
    if led and board:
        led.set_board(board)
        led.setup_led(13)
        led.blink(13, times=5)
```

### Complete Script Example

Here's a complete traffic light simulation script:

```python
"""
Traffic Light Simulation Script

Hardware setup:
- Red LED on pin 2
- Yellow LED on pin 3
- Green LED on pin 4

This script uses the LEDController plugin to simulate a traffic light.
"""

import time

# Configuration
RED_PIN = 2
YELLOW_PIN = 3
GREEN_PIN = 4

# Timing (in seconds)
GREEN_TIME = 5
YELLOW_TIME = 2
RED_TIME = 5

# Global variable for cleanup
_led = None


def main(plugins):
    """Run the traffic light simulation"""
    global _led
    
    print("=" * 50)
    print("Traffic Light Simulation")
    print("=" * 50)
    
    # Get plugins
    board = plugins.get("telemetrix")
    _led = plugins.get("ledcontroller")
    
    if not board:
        print("ERROR: Telemetrix board not connected")
        return
    
    if not _led:
        print("ERROR: LEDController plugin not found")
        print("Please install ledcontroller plugin")
        return
    
    # Initialize LED controller
    _led.set_board(board)
    
    # Setup LEDs
    print("\nSetting up LEDs...")
    _led.setup_led(RED_PIN)
    _led.setup_led(YELLOW_PIN)
    _led.setup_led(GREEN_PIN)
    
    # Run traffic light cycle
    print("\nStarting traffic light cycle...")
    print("Press Stop button to end simulation\n")
    
    try:
        cycle_count = 0
        while True:
            cycle_count += 1
            print(f"--- Cycle {cycle_count} ---")
            
            # Green light
            print("GREEN light")
            _led.turn_on(GREEN_PIN)
            time.sleep(GREEN_TIME)
            _led.turn_off(GREEN_PIN)
            
            # Yellow light
            print("YELLOW light")
            _led.turn_on(YELLOW_PIN)
            time.sleep(YELLOW_TIME)
            _led.turn_off(YELLOW_PIN)
            
            # Red light
            print("RED light")
            _led.turn_on(RED_PIN)
            time.sleep(RED_TIME)
            _led.turn_off(RED_PIN)
            
    except KeyboardInterrupt:
        print("\nSimulation interrupted")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        cleanup()


def stop():
    """Clean up when stopped"""
    print("\nStopping traffic light simulation...")
    cleanup()


def cleanup():
    """Turn off all LEDs"""
    global _led
    if _led:
        _led.turn_off(RED_PIN)
        _led.turn_off(YELLOW_PIN)
        _led.turn_off(GREEN_PIN)
        print("All LEDs turned off")
```

### Saving Your Script

1. Save your script file with a descriptive name: `my_script.py`
2. Copy it to the BrightOS Scripts directory:
   - **Windows**: `%USERPROFILE%\AppData\Local\BrightOS\Scripts\`
   - **Linux/macOS**: `~/.brightos/Scripts/`
3. Restart BrightOS
4. Your script will appear in the dropdown menu

---

## Best Practices

### For Plugins

1. **Always check if board is connected** before using it
2. **Use descriptive method names** that clearly indicate what they do
3. **Include docstrings** for all public methods
4. **Handle errors gracefully** with try/except blocks
5. **Provide feedback** using `self.print()` and `self.eprint()`
6. **Keep track of state** (which pins are configured, current positions, etc.)
7. **Provide cleanup methods** to safely stop operations

```python
# Good example
def servo_control(self, pin, angle):
    """Move servo to specified angle"""
    if not self._board:
        self.eprint("Board not connected")
        return False
    
    if not 0 <= angle <= 180:
        self.eprint(f"Invalid angle: {angle}")
        return False
    
    try:
        self._board.servo_write(pin, angle)
        return True
    except Exception as e:
        self.eprint(f"Error: {e}")
        return False
```

### For Scripts

1. **Always check for required plugins** before using them
2. **Implement the stop() function** for proper cleanup
3. **Use constants** for pin numbers and configuration
4. **Add comments** explaining hardware setup
5. **Handle exceptions** to prevent crashes
6. **Provide user feedback** with print statements
7. **Test thoroughly** before sharing

```python
# Good example
def main(plugins):
    # Check dependencies
    board = plugins.get("telemetrix")
    if not board:
        print("ERROR: Board not connected")
        return
    
    # Use constants
    SERVO_PIN = 9
    
    # Provide feedback
    print("Starting script...")
    
    # Handle errors
    try:
        # Your code
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        print("Cleanup complete")
```

### Code Style

- Use descriptive variable names
- Add type hints where helpful
- Follow PEP 8 style guidelines
- Keep functions focused on one task
- Comment complex logic

---

## Testing Your Code

### Testing Plugins

Test your plugin without a real board using a mock:

```python
# test_my_plugin.py
from my_plugin import MyPlugin

# Create plugin instance
plugin = MyPlugin()

# Test without board (should handle gracefully)
result = plugin.my_function(10, 20)
print(f"Without board: {result}")  # Should be False

# Test with mock board
class MockBoard:
    def set_pin_mode_digital_output(self, pin):
        print(f"Mock: Set pin {pin} to output")

plugin.set_board(MockBoard())
result = plugin.my_function(10, 20)
print(f"With mock board: {result}")  # Should work
```

### Testing Scripts

Test your script's structure:

```python
# test_my_script.py
import my_script

# Check required functions exist
assert hasattr(my_script, 'main'), "Missing main() function"
assert hasattr(my_script, 'stop'), "Missing stop() function"

# Test with mock plugins
mock_plugins = {
    "telemetrix": None,
    "myplugn": None
}

# This should handle missing board gracefully
my_script.main(mock_plugins)
```

### Integration Testing

1. Start BrightOS
   - **Auto-connection**: Set `ARDUINO_IP_ADDRESS` environment variable before launching
   - **Manual connection**: Use "Configure Telemetrix" button after launching
2. Load your plugin/script
3. Run with minimal hardware first
4. Test error cases (disconnect, invalid values)
5. Test the stop() function
6. Verify cleanup happens correctly

---

## Sharing Your Work

### Preparing to Share

1. **Add documentation** at the top of your file
2. **Include hardware requirements**
3. **List dependencies** (required plugins)
4. **Add usage examples**
5. **Test thoroughly**

### Documentation Template

```python
"""
[Plugin/Script Name]

Description:
    Brief description of what this does.

Hardware Setup:
    - Component 1 on pin X
    - Component 2 on pin Y

Requirements:
    - BrightOS with Telemetrix
    - [List any required plugins]
    
Usage:
    [Brief usage example]

Author: Your Name
Version: 1.0
"""
```

### Contributing

To share with the community:

1. Fork the [BrightOS repository](https://github.com/TheCrazy8/Blaze-And-Company-Official)
2. Add your plugin to `community made plugins/` or script to `community made scripts/`
3. Update the respective README.md
4. Create a pull request

Include in your pull request:
- Clear description of what your code does
- Hardware requirements
- Any dependencies
- Testing you've done

---

## Additional Resources

- [Downloads Page](/downloads) - Get existing plugins and scripts
- [BrightOS Documentation](/) - Learn more about BrightOS
- [Example Plugin](https://github.com/TheCrazy8/Blaze-And-Company-Official/blob/main/community%20made%20plugins/motor_controller_plugin.py) - See a complete plugin
- [Example Script](https://github.com/TheCrazy8/Blaze-And-Company-Official/blob/main/community%20made%20scripts/motor_example.py) - See a complete script

## Need Help?

- Check existing plugins and scripts for examples
- Review the [Telemetrix documentation](https://mryslab.github.io/telemetrix-uno-r4/)
- Ask in the [GitHub Discussions](https://github.com/TheCrazy8/Blaze-And-Company-Official/discussions)

Happy coding! 🚀
