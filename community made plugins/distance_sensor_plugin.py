"""
Distance Sensor Plugin for BrightOS

This plugin provides functions for reading distance measurements from ultrasonic sensors
(HC-SR04 and compatible models) connected to Arduino pins.

Example usage in a script:
    def main(plugins):
        distance = plugins.get("distancesensor")
        if distance:
            # Setup ultrasonic sensor on pins 8 (trigger) and 9 (echo)
            distance.setup_ultrasonic(8, 9)
            
            # Get distance reading in centimeters
            cm = distance.read_distance(8)
            print(f"Distance: {cm} cm")
            
            # Get distance in inches
            inches = distance.read_distance_inches(8)
            print(f"Distance: {inches} inches")
            
            # Check if object is within range
            if distance.is_in_range(8, 10, 50):
                print("Object detected in range!")
"""

from simple_plugin_loader.sample_plugin import SamplePlugin
import time


class DistanceSensor(SamplePlugin):
    """
    A plugin for reading distance measurements from ultrasonic sensors.
    Requires a telemetrix board connection to function.
    """
    
    def __init__(self):
        """Initialize the distance sensor plugin"""
        self._board = None
        self._sensors = {}  # Track configured sensors
        self._last_readings = {}  # Store last distance readings
        
    def set_board(self, board):
        """
        Set the telemetrix board instance for sensor control
        
        Args:
            board: TelemetrixUnoR4WiFi board instance
        """
        self._board = board
        
    def setup_ultrasonic(self, trigger_pin, echo_pin):
        """
        Configure an ultrasonic distance sensor (HC-SR04 compatible).
        
        Args:
            trigger_pin (int): Arduino pin connected to sensor trigger
            echo_pin (int): Arduino pin connected to sensor echo
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            distance.setup_ultrasonic(8, 9)  # Trigger on pin 8, echo on pin 9
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        try:
            # Set trigger pin as output
            self._board.set_pin_mode_digital_output(trigger_pin)
            
            # Set echo pin as input
            self._board.set_pin_mode_digital_input(echo_pin)
            
            # Store sensor configuration
            self._sensors[trigger_pin] = {
                "echo_pin": echo_pin,
                "type": "ultrasonic"
            }
            self._last_readings[trigger_pin] = 0
            
            self.print(f"Ultrasonic sensor configured: trigger={trigger_pin}, echo={echo_pin}")
            return True
            
        except Exception as e:
            self.eprint(f"Error setting up ultrasonic sensor: {e}")
            return False
    
    def _read_ultrasonic(self, trigger_pin):
        """
        Internal method to read ultrasonic sensor.
        Returns distance in centimeters.
        
        NOTE: This is a placeholder implementation. For actual distance readings,
        Telemetrix should have built-in sonar support. Check your Telemetrix 
        documentation for the proper sonar implementation for your board.
        
        If your board doesn't support sonar mode, you'll need to implement
        pulse timing measurement on the Arduino side and read the results.
        """
        if trigger_pin not in self._sensors:
            return None
            
        echo_pin = self._sensors[trigger_pin]["echo_pin"]
        
        # NOTE: This implementation is incomplete and returns placeholder values.
        # For actual sensor readings, implement one of these approaches:
        # 1. Use Telemetrix's built-in sonar support if available
        # 2. Create custom Arduino firmware that measures pulse duration
        # 3. Use interrupt-based timing measurement
        
        # Return None to indicate no valid reading
        # Users should implement proper sonar support based on their hardware
        self.eprint("Warning: Ultrasonic sensor requires Telemetrix sonar support.")
        self.eprint("Implementation options:")
        self.eprint("  1. Use board.set_pin_mode_sonar() if available in your Telemetrix version")
        self.eprint("  2. Implement pulse timing in Arduino firmware and read via callbacks")
        self.eprint("  3. Check Telemetrix documentation for your specific board model")
        return None
    
    def read_distance(self, trigger_pin, num_samples=1):
        """
        Read distance from ultrasonic sensor in centimeters.
        
        Args:
            trigger_pin (int): Trigger pin of the sensor
            num_samples (int): Number of readings to average (default: 1)
            
        Returns:
            float: Distance in centimeters, or None if error
            
        Example:
            cm = distance.read_distance(8)
            print(f"Distance: {cm} cm")
            
            # Average 5 readings for more accuracy
            cm = distance.read_distance(8, num_samples=5)
        """
        if not self._board or trigger_pin not in self._sensors:
            self.eprint(f"Sensor on pin {trigger_pin} not configured")
            return None
        
        if self._sensors[trigger_pin]["type"] != "ultrasonic":
            self.eprint(f"Pin {trigger_pin} is not configured as ultrasonic sensor")
            return None
        
        readings = []
        for _ in range(num_samples):
            reading = self._read_ultrasonic(trigger_pin)
            if reading is not None:
                readings.append(reading)
            time.sleep(0.06)  # Wait between readings (minimum 60ms for HC-SR04)
        
        if not readings:
            return None
        
        # Calculate average
        avg_distance = sum(readings) / len(readings)
        self._last_readings[trigger_pin] = avg_distance
        
        return avg_distance
    
    def read_distance_inches(self, trigger_pin, num_samples=1):
        """
        Read distance from ultrasonic sensor in inches.
        
        Args:
            trigger_pin (int): Trigger pin of the sensor
            num_samples (int): Number of readings to average (default: 1)
            
        Returns:
            float: Distance in inches, or None if error
            
        Example:
            inches = distance.read_distance_inches(8)
            print(f"Distance: {inches} inches")
        """
        cm = self.read_distance(trigger_pin, num_samples)
        if cm is not None:
            return cm / 2.54
        return None
    
    def is_in_range(self, trigger_pin, min_cm, max_cm):
        """
        Check if an object is within a specified distance range.
        
        Args:
            trigger_pin (int): Trigger pin of the sensor
            min_cm (float): Minimum distance in centimeters
            max_cm (float): Maximum distance in centimeters
            
        Returns:
            bool: True if object is in range, False otherwise
            
        Example:
            # Check if object is between 10cm and 50cm away
            if distance.is_in_range(8, 10, 50):
                print("Object in range!")
        """
        reading = self.read_distance(trigger_pin)
        if reading is None:
            return False
        
        return min_cm <= reading <= max_cm
    
    def wait_for_object(self, trigger_pin, max_distance_cm, timeout=10):
        """
        Wait for an object to come within a specified distance.
        
        Args:
            trigger_pin (int): Trigger pin of the sensor
            max_distance_cm (float): Maximum distance in centimeters
            timeout (float): Maximum time to wait in seconds (default: 10)
            
        Returns:
            bool: True if object detected, False if timeout
            
        Example:
            # Wait up to 30 seconds for object within 30cm
            if distance.wait_for_object(8, 30, timeout=30):
                print("Object detected!")
            else:
                print("Timeout - no object detected")
        """
        start_time = time.time()
        
        while (time.time() - start_time) < timeout:
            reading = self.read_distance(trigger_pin)
            if reading is not None and reading <= max_distance_cm:
                self.print(f"Object detected at {reading:.1f}cm")
                return True
            time.sleep(0.1)
        
        self.print(f"Timeout waiting for object")
        return False
    
    def get_last_reading(self, trigger_pin):
        """
        Get the last distance reading without taking a new measurement.
        
        Args:
            trigger_pin (int): Trigger pin of the sensor
            
        Returns:
            float: Last distance reading in centimeters, or None if no reading
            
        Example:
            last = distance.get_last_reading(8)
            print(f"Last reading: {last} cm")
        """
        return self._last_readings.get(trigger_pin)
    
    def monitor_distance(self, trigger_pin, duration=10, interval=0.5):
        """
        Monitor distance continuously for a specified duration.
        Prints readings at regular intervals.
        
        Args:
            trigger_pin (int): Trigger pin of the sensor
            duration (float): Duration to monitor in seconds (default: 10)
            interval (float): Time between readings in seconds (default: 0.5)
            
        Returns:
            list: List of distance readings
            
        Example:
            # Monitor for 30 seconds, reading every second
            readings = distance.monitor_distance(8, duration=30, interval=1.0)
            print(f"Average distance: {sum(readings)/len(readings):.1f}cm")
        """
        if not self._board or trigger_pin not in self._sensors:
            self.eprint(f"Sensor on pin {trigger_pin} not configured")
            return []
        
        readings = []
        start_time = time.time()
        
        self.print(f"Starting distance monitoring for {duration} seconds...")
        
        while (time.time() - start_time) < duration:
            reading = self.read_distance(trigger_pin)
            if reading is not None:
                readings.append(reading)
                self.print(f"Distance: {reading:.1f}cm")
            time.sleep(interval)
        
        if readings:
            avg = sum(readings) / len(readings)
            min_dist = min(readings)
            max_dist = max(readings)
            self.print(f"Monitoring complete: avg={avg:.1f}cm, min={min_dist:.1f}cm, max={max_dist:.1f}cm")
        
        return readings
    
    def cleanup(self):
        """Clean up sensor configurations"""
        self._sensors.clear()
        self._last_readings.clear()
        self.print("Distance sensor plugin cleanup completed")
