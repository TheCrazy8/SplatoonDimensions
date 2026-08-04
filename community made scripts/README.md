# Community Made Scripts

This directory contains community-contributed scripts for BrightOS. Scripts are Python programs that run on BrightOS and can use plugins to interact with hardware.

## What are Scripts?

Scripts are Python modules that contain a `main()` function. They are loaded by BrightOS and can be selected and run from the GUI.

## Installing Scripts

1. Download the script file (`.py` file)
2. Copy it to your BrightOS Scripts directory:
   - **Windows**: `%USERPROFILE%\AppData\Local\BrightOS\Scripts\`
   - **Linux/macOS**: `~/.brightos/Scripts/`
3. Restart BrightOS - the script will appear in the script selection dropdown

## Script Structure

A basic BrightOS script looks like this:

```python
def main(plugins):
    """
    Main function that runs when the script is executed.
    
    Args:
        plugins: Dictionary containing loaded plugins including 'telemetrix' board
    """
    # Get the telemetrix board
    board = plugins.get("telemetrix")
    
    if not board:
        print("Telemetrix board not connected")
        return
    
    # Your script code here
    print("Script running!")

def stop():
    """
    Optional: Called when the user clicks the Stop button.
    Use this to clean up resources and stop any running operations.
    """
    print("Script stopped")
```

## Available Scripts

### examplescript.py
Basic example showing how to use the Telemetrix board to display a message on an Arduino LED matrix.

**Download:** [examplescript.py](examplescript.py)

### motor_example.py
Comprehensive example demonstrating motor control using the MotorController plugin.

**Features:**
- Servo position control
- DC motor speed control with optional direction control
- Servo sweep demonstration
- DC motor speed ramping

**Requirements:**
- MotorController plugin installed
- Servo motor connected to pin 9
- DC motor connected to PWM pin 5 (optional direction pin 4)

**Download:** [motor_example.py](motor_example.py)

## Using Plugins in Scripts

Scripts can use any loaded plugins:

```python
def main(plugins):
    # Get the telemetrix board
    board = plugins.get("telemetrix")
    
    # Get a custom plugin (note: plugin keys are lowercase)
    motor = plugins.get("motorcontroller")
    
    if motor and board:
        motor.set_board(board)
        motor.servo_control(9, 90)
```

## Creating Your Own Scripts

1. Create a new Python file in this directory
2. Implement a `main(plugins)` function
3. Optionally implement a `stop()` function for cleanup
4. Save the file and restart BrightOS

Example template:

```python
import time

def main(plugins):
    board = plugins.get("telemetrix")
    
    if not board:
        print("ERROR: Telemetrix board not connected")
        return
    
    print("My script is running!")
    
    # Your code here
    
    print("Script completed")

def stop():
    print("Cleaning up...")
    # Stop any running operations
```

## Contributing

To share your script with the community:
1. Create a pull request to add your script to this directory
2. Include documentation in this README
3. Test your script thoroughly before submitting
4. Include comments explaining what your script does
