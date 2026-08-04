"""
Plugin Usage Examples for BrightOS

This script demonstrates how to use the new sensor and hardware plugins.
This is a reference guide showing various plugin capabilities.
"""

def electromagnet_example(plugins):
    """Example: Control an electromagnet"""
    magnet = plugins.get("electromagnet")
    if magnet:
        # Setup and activate electromagnet
        magnet.activate(7, strength=100)  # Pin 7, full strength
        # Hold for 3 seconds
        import time
        time.sleep(3)
        magnet.deactivate(7)
        print("Electromagnet demo complete")

def distance_sensor_example(plugins):
    """Example: Read distance from ultrasonic sensor"""
    distance = plugins.get("distancesensor")
    if distance:
        # Setup HC-SR04: trigger on pin 8, echo on pin 9
        distance.setup_ultrasonic(8, 9)
        
        # Read distance
        cm = distance.read_distance(8)
        print(f"Distance: {cm} cm")
        
        # Check if object in range
        if distance.is_in_range(8, 10, 50):
            print("Object detected in range!")

def temperature_sensor_example(plugins):
    """Example: Read temperature and humidity"""
    temp = plugins.get("temperaturesensor")
    if temp:
        # Setup DHT22 on pin 2
        temp.setup_dht(2, "DHT22")
        
        # Read temperature and humidity
        temp_c, humidity = temp.read_temperature_humidity(2)
        print(f"Temperature: {temp_c}°C")
        print(f"Humidity: {humidity}%")
        
        # Check comfort level
        comfort = temp.is_comfortable(2)
        if comfort['overall']:
            print("Conditions are comfortable!")

def light_sensor_example(plugins):
    """Example: Monitor light levels"""
    light = plugins.get("lightsensor")
    if light:
        # Setup on analog pin A0
        light.setup_sensor(0)
        
        # Read light level
        percent = light.read_light_percent(0)
        print(f"Light level: {percent}%")
        
        # Check if dark
        if light.is_dark(0, threshold=20):
            print("It's dark - turning on lights!")

def motion_sensor_example(plugins):
    """Example: Detect motion with PIR sensor"""
    motion = plugins.get("motionsensor")
    if motion:
        # Setup PIR on pin 7
        motion.setup_pir(7)
        
        # Wait for sensor to stabilize
        motion.wait_until_ready(7)
        
        # Check for motion
        if motion.is_motion_detected(7):
            print("Motion detected!")
        
        # Wait for motion event
        if motion.wait_for_motion(7, timeout=30):
            print("Someone moved!")

def sound_sensor_example(plugins):
    """Example: Detect sound levels"""
    sound = plugins.get("soundsensor")
    if sound:
        # Setup analog sound sensor on A1
        sound.setup_analog(1)
        
        # Read sound level
        level = sound.read_sound_percent(1)
        print(f"Sound level: {level}%")
        
        # Wait for loud sound
        if sound.wait_for_sound(1, threshold=70, timeout=10):
            print("Loud sound detected!")

def button_example(plugins):
    """Example: Read button input"""
    button = plugins.get("button")
    if button:
        # Setup button on pin 2 with pull-up
        button.setup_button(2, pull_up=True)
        
        # Wait for button press
        print("Press the button...")
        if button.wait_for_press(2, timeout=10):
            print("Button pressed!")
        
        # Detect double-click
        clicks = button.count_clicks(2, timeout=3)
        if clicks == 2:
            print("Double click detected!")

def buzzer_example(plugins):
    """Example: Play sounds with buzzer"""
    buzzer = plugins.get("buzzer")
    if buzzer:
        # Setup buzzer on pin 8
        buzzer.setup_buzzer(8)
        
        # Play a tone
        buzzer.play_tone(8, 440, duration=1.0)  # A4 note
        
        # Play a melody
        buzzer.play_melody(8, "CDEFGABC")
        
        # Make beeps
        buzzer.beep(8, times=3)

def main(plugins):
    """Main function demonstrating all plugins"""
    print("=== BrightOS Plugin Examples ===")
    print("This script shows how to use the new plugins.")
    print("Uncomment the example you want to run:")
    
    # Uncomment the example you want to try:
    # electromagnet_example(plugins)
    # distance_sensor_example(plugins)
    # temperature_sensor_example(plugins)
    # light_sensor_example(plugins)
    # motion_sensor_example(plugins)
    # sound_sensor_example(plugins)
    # button_example(plugins)
    # buzzer_example(plugins)
    
    print("\nTo use these plugins, uncomment the desired example in the script.")
