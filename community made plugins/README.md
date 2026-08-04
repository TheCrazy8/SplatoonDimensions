# Community Made Plugins

This directory contains community-contributed plugins for BrightOS. Plugins are classes that extend BrightOS functionality and can be used by scripts.

## What are Plugins?

Plugins are Python classes that inherit from `SamplePlugin` and provide reusable functionality. They are loaded automatically by BrightOS and made available to all scripts through the `plugins` dictionary.

## Installing Plugins

1. Download the plugin file (`.py` file)
2. Copy it to your BrightOS Plugins directory:
   - **Windows**: `%USERPROFILE%\AppData\Local\BrightOS\Plugins\`
   - **Linux/macOS**: `~/.brightos/Plugins/`
3. Restart BrightOS - the plugin will be loaded automatically

## Using Plugins in Scripts

```python
def main(plugins):
    # Get a plugin by its class name (lowercase)
    my_plugin = plugins.get("pluginclassname")
    
    if my_plugin:
        # Use the plugin's methods
        my_plugin.some_method()
```

## Available Plugins

### LEDController
Control LEDs connected to Arduino pins with support for on/off, blinking, and fading.

**Key Functions:**
- `setup_led(pin, pwm=False)` - Configure LED pin
- `turn_on(pin, brightness=100)` - Turn on LED with optional brightness
- `turn_off(pin)` - Turn off LED
- `blink(pin, times=3, interval=0.5)` - Blink LED
- `fade(pin, start=0, end=100)` - Fade LED brightness

**Download:** [led_controller_plugin.py](led_controller_plugin.py)

### MotorController
Control various types of motors (servos, DC motors) connected to Arduino.

**Key Functions:**
- `servo_control(pin, angle)` - Control servo position
- `dc_motor_control(pin, speed_percent)` - Control DC motor speed
- `stop_motor(pin, motor_type)` - Stop a specific motor
- `stop_all()` - Stop all motors
- `get_servo_position(pin)` - Get current servo position
- `sweep_servo(pin, start_angle, end_angle)` - Sweep servo back and forth
- `ramp_dc_motor(pin, start_speed, end_speed)` - Gradually ramp motor speed

**Download:** [motor_controller_plugin.py](motor_controller_plugin.py)

### Electromagnet
Control electromagnets with support for variable strength, timed operations, and pulsing.

**Key Functions:**
- `setup_magnet(pin, pwm=False)` - Configure electromagnet pin
- `activate(pin, strength=100)` - Turn on electromagnet at specified strength
- `deactivate(pin)` - Turn off electromagnet
- `activate_timed(pin, duration, strength=100)` - Activate for specific duration
- `pulse(pin, on_time=0.5, off_time=0.5, cycles=3)` - Pulse electromagnet
- `ramp_strength(pin, start=0, end=100)` - Gradually change strength
- `is_active(pin)` - Check if electromagnet is active
- `deactivate_all()` - Emergency stop all electromagnets

**Download:** [electromagnet_plugin.py](electromagnet_plugin.py)

### DistanceSensor
Read distance measurements from ultrasonic sensors (HC-SR04 compatible).

**Key Functions:**
- `setup_ultrasonic(trigger_pin, echo_pin)` - Configure ultrasonic sensor
- `read_distance(pin, num_samples=1)` - Read distance in centimeters
- `read_distance_inches(pin)` - Read distance in inches
- `is_in_range(pin, min_cm, max_cm)` - Check if object is in range
- `wait_for_object(pin, max_distance_cm, timeout=10)` - Wait for object detection
- `monitor_distance(pin, duration=10)` - Continuously monitor distance

**Download:** [distance_sensor_plugin.py](distance_sensor_plugin.py)

### TemperatureSensor
Read temperature and humidity from DHT sensors (DHT11, DHT22/AM2302).

**Key Functions:**
- `setup_dht(pin, sensor_type="DHT22")` - Configure DHT sensor
- `read_temperature(pin)` - Read temperature in Celsius
- `read_temperature_fahrenheit(pin)` - Read temperature in Fahrenheit
- `read_humidity(pin)` - Read humidity percentage
- `read_temperature_humidity(pin)` - Read both values at once
- `calculate_heat_index(pin)` - Calculate heat index (feels-like temperature)
- `calculate_dew_point(pin)` - Calculate dew point
- `monitor_conditions(pin, duration=60)` - Monitor environmental conditions
- `is_comfortable(pin)` - Check if conditions are in comfortable range

**Download:** [temperature_sensor_plugin.py](temperature_sensor_plugin.py)

### LightSensor
Read light levels from photoresistors (LDR) and analog light sensors.

**Key Functions:**
- `setup_sensor(analog_pin)` - Configure light sensor on analog pin
- `read_light_level(pin)` - Read raw light level (0-1023)
- `read_light_percent(pin)` - Read light level as percentage
- `calibrate(pin, mode="dark")` - Calibrate for dark or bright conditions
- `is_dark(pin, threshold=20)` - Check if dark
- `is_bright(pin, threshold=80)` - Check if bright
- `wait_for_dark(pin)` - Wait until dark
- `wait_for_bright(pin)` - Wait until bright
- `monitor_light(pin, duration=60)` - Monitor light levels
- `detect_light_change(pin)` - Detect significant light changes

**Download:** [light_sensor_plugin.py](light_sensor_plugin.py)

### MotionSensor
Detect motion using PIR (Passive Infrared) sensors.

**Key Functions:**
- `setup_pir(pin)` - Configure PIR motion sensor
- `is_motion_detected(pin)` - Check if motion is currently detected
- `wait_for_motion(pin, timeout=30)` - Wait for motion detection
- `wait_for_no_motion(pin, timeout=30)` - Wait for motion to stop
- `monitor_motion(pin, duration=60)` - Monitor and count motion events
- `get_motion_count(pin)` - Get total motion event count
- `is_sensor_ready(pin)` - Check if PIR sensor is warmed up
- `wait_until_ready(pin)` - Wait for PIR warmup period
- `detect_presence(pin)` - Check if someone is present in area

**Download:** [motion_sensor_plugin.py](motion_sensor_plugin.py)

### SoundSensor
Detect and measure sound levels using microphone modules.

**Key Functions:**
- `setup_analog(analog_pin)` - Configure analog sound sensor
- `setup_digital(pin)` - Configure digital sound sensor
- `read_sound_level(pin)` - Read sound level value
- `read_sound_percent(pin)` - Read sound as percentage
- `calibrate_baseline(pin, duration=2)` - Calibrate ambient sound level
- `is_loud(pin, threshold=70)` - Check if sound exceeds threshold
- `wait_for_sound(pin, threshold=70)` - Wait for loud sound
- `wait_for_quiet(pin)` - Wait for quiet conditions
- `monitor_sound(pin, duration=60)` - Monitor sound levels
- `detect_clap(pin)` - Detect clap or sudden loud sound

**Download:** [sound_sensor_plugin.py](sound_sensor_plugin.py)

### Button
Read button presses and switch states from digital input devices.

**Key Functions:**
- `setup_button(pin, pull_up=True)` - Configure button/switch pin
- `is_pressed(pin)` - Check if button is pressed
- `is_released(pin)` - Check if button is released
- `wait_for_press(pin, timeout=None)` - Wait for button press
- `wait_for_release(pin)` - Wait for button release
- `wait_for_click(pin)` - Wait for complete press and release
- `get_press_count(pin)` - Get total press count
- `detect_long_press(pin, duration=2.0)` - Detect long press
- `count_clicks(pin, timeout=3.0)` - Count multiple clicks (double-click, etc.)
- `read_switch_state(pin)` - Read toggle switch state
- `wait_for_state_change(pin)` - Wait for any state change

**Download:** [button_plugin.py](button_plugin.py)

### Buzzer
Control buzzers and speakers with tone generation, melodies, and sound patterns.

**Key Functions:**
- `setup_buzzer(pin)` - Configure buzzer pin
- `play_tone(pin, frequency, duration=1.0)` - Play tone at frequency
- `play_note(pin, note, duration=0.5)` - Play musical note (e.g., "C4", "A4")
- `play_melody(pin, notes, tempo=120)` - Play melody from note string
- `beep(pin, times=1, duration=0.1)` - Make beeping sounds
- `alarm(pin, duration=5)` - Play alarm pattern
- `siren(pin, duration=5)` - Play siren pattern
- `chirp(pin)` - Make quick chirp sound
- `buzzer_morse(pin, message, wpm=15)` - Play Morse code
- `play_rtttl(pin, rtttl_string)` - Play RTTTL format melodies
- `stop(pin)` - Stop buzzer

**Download:** [buzzer_plugin.py](buzzer_plugin.py)

## Creating Your Own Plugins

To create a plugin:

1. Create a new Python file in this directory
2. Import the base class: `from simple_plugin_loader.sample_plugin import SamplePlugin`
3. Create a class that inherits from `SamplePlugin`:

```python
from simple_plugin_loader.sample_plugin import SamplePlugin

class MyPlugin(SamplePlugin):
    def __init__(self):
        # Initialize your plugin
        pass
    
    def my_function(self):
        # Your plugin functionality
        self.print("Hello from my plugin!")
```

4. Save the file and restart BrightOS

## Contributing

To share your plugin with the community:
1. Create a pull request to add your plugin to this directory
2. Include documentation in this README
3. Follow the existing plugin structure and style
