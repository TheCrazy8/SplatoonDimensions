"""
Light Sensor Plugin for BrightOS

This plugin provides functions for reading light levels from photoresistors (LDR)
and other analog light sensors connected to Arduino analog pins.

Example usage in a script:
    def main(plugins):
        light = plugins.get("lightsensor")
        if light:
            # Setup light sensor on analog pin A0
            light.setup_sensor(0)
            
            # Read raw light level (0-1023)
            level = light.read_light_level(0)
            print(f"Light level: {level}")
            
            # Read as percentage
            percent = light.read_light_percent(0)
            print(f"Light: {percent}%")
            
            # Check if it's dark
            if light.is_dark(0, threshold=20):
                print("It's dark - turning on lights!")
"""

from simple_plugin_loader.sample_plugin import SamplePlugin
import time


class LightSensor(SamplePlugin):
    """
    A plugin for reading light levels from photoresistors and light sensors.
    Requires a telemetrix board connection to function.
    """
    
    def __init__(self):
        """Initialize the light sensor plugin"""
        self._board = None
        self._sensors = {}  # Track configured sensors
        self._last_readings = {}  # Store last light readings
        self._callbacks = {}  # Store callback data
        
    def set_board(self, board):
        """
        Set the telemetrix board instance for sensor control
        
        Args:
            board: TelemetrixUnoR4WiFi board instance
        """
        self._board = board
        
    def _analog_callback(self, data):
        """Internal callback for analog readings"""
        pin = data[1]
        value = data[2]
        if pin in self._callbacks:
            self._last_readings[pin] = value
    
    def setup_sensor(self, analog_pin):
        """
        Configure an analog pin for light sensor reading.
        
        Args:
            analog_pin (int): Arduino analog pin (0-5 for A0-A5)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            light.setup_sensor(0)   # Setup sensor on A0
            light.setup_sensor(2)   # Setup sensor on A2
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        try:
            # Configure analog input pin
            self._board.set_pin_mode_analog_input(analog_pin, callback=self._analog_callback)
            
            # Store sensor configuration
            self._sensors[analog_pin] = {
                "type": "photoresistor",
                "calibration_dark": 0,
                "calibration_bright": 1023
            }
            self._last_readings[analog_pin] = 0
            self._callbacks[analog_pin] = True
            
            self.print(f"Light sensor configured on analog pin A{analog_pin}")
            return True
            
        except Exception as e:
            self.eprint(f"Error setting up light sensor on pin A{analog_pin}: {e}")
            return False
    
    def read_light_level(self, analog_pin):
        """
        Read raw light level from sensor (0-1023).
        Higher values typically indicate more light.
        
        Args:
            analog_pin (int): Arduino analog pin (0-5 for A0-A5)
            
        Returns:
            int: Light level (0-1023), or None if error
            
        Example:
            level = light.read_light_level(0)
            print(f"Raw light level: {level}")
        """
        if not self._board or analog_pin not in self._sensors:
            self.eprint(f"Sensor on pin A{analog_pin} not configured")
            return None
        
        # Wait a moment for callback to update reading
        time.sleep(0.05)
        
        return self._last_readings.get(analog_pin, 0)
    
    def read_light_percent(self, analog_pin):
        """
        Read light level as a percentage (0-100%).
        Uses calibration values if set, otherwise uses full range.
        
        Args:
            analog_pin (int): Arduino analog pin (0-5 for A0-A5)
            
        Returns:
            float: Light level percentage (0-100), or None if error
            
        Example:
            percent = light.read_light_percent(0)
            print(f"Light level: {percent:.1f}%")
        """
        raw_value = self.read_light_level(analog_pin)
        if raw_value is None:
            return None
        
        sensor = self._sensors[analog_pin]
        dark_val = sensor["calibration_dark"]
        bright_val = sensor["calibration_bright"]
        
        # Calculate percentage based on calibration
        range_val = bright_val - dark_val
        if range_val == 0:
            return 0.0
        
        percent = ((raw_value - dark_val) / range_val) * 100.0
        # Clamp to 0-100 range
        return max(0.0, min(100.0, percent))
    
    def calibrate(self, analog_pin, mode="dark"):
        """
        Calibrate the sensor for dark or bright conditions.
        
        Args:
            analog_pin (int): Arduino analog pin (0-5 for A0-A5)
            mode (str): "dark" or "bright" - which condition to calibrate
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            # Cover sensor and calibrate dark
            light.calibrate(0, "dark")
            
            # Shine bright light and calibrate bright
            light.calibrate(0, "bright")
        """
        if not self._board or analog_pin not in self._sensors:
            self.eprint(f"Sensor on pin A{analog_pin} not configured")
            return False
        
        mode = mode.lower()
        if mode not in ["dark", "bright"]:
            self.eprint("Mode must be 'dark' or 'bright'")
            return False
        
        # Take multiple readings and average
        readings = []
        for _ in range(10):
            reading = self.read_light_level(analog_pin)
            if reading is not None:
                readings.append(reading)
            time.sleep(0.1)
        
        if not readings:
            self.eprint("Failed to get calibration readings")
            return False
        
        avg_value = sum(readings) // len(readings)
        
        if mode == "dark":
            self._sensors[analog_pin]["calibration_dark"] = avg_value
            self.print(f"Dark calibration set to {avg_value} on pin A{analog_pin}")
        else:
            self._sensors[analog_pin]["calibration_bright"] = avg_value
            self.print(f"Bright calibration set to {avg_value} on pin A{analog_pin}")
        
        return True
    
    def is_dark(self, analog_pin, threshold=20):
        """
        Check if the light level is below a threshold (dark condition).
        
        Args:
            analog_pin (int): Arduino analog pin (0-5 for A0-A5)
            threshold (float): Light percentage threshold (default: 20%)
            
        Returns:
            bool: True if dark, False otherwise
            
        Example:
            if light.is_dark(0, threshold=15):
                print("It's dark!")
        """
        percent = self.read_light_percent(analog_pin)
        if percent is None:
            return False
        return percent < threshold
    
    def is_bright(self, analog_pin, threshold=80):
        """
        Check if the light level is above a threshold (bright condition).
        
        Args:
            analog_pin (int): Arduino analog pin (0-5 for A0-A5)
            threshold (float): Light percentage threshold (default: 80%)
            
        Returns:
            bool: True if bright, False otherwise
            
        Example:
            if light.is_bright(0, threshold=85):
                print("It's very bright!")
        """
        percent = self.read_light_percent(analog_pin)
        if percent is None:
            return False
        return percent > threshold
    
    def wait_for_dark(self, analog_pin, threshold=20, timeout=30):
        """
        Wait for light level to drop below threshold.
        
        Args:
            analog_pin (int): Arduino analog pin (0-5 for A0-A5)
            threshold (float): Light percentage threshold (default: 20%)
            timeout (float): Maximum time to wait in seconds (default: 30)
            
        Returns:
            bool: True if dark condition reached, False if timeout
            
        Example:
            if light.wait_for_dark(0, threshold=25, timeout=60):
                print("It got dark!")
        """
        start_time = time.time()
        
        while (time.time() - start_time) < timeout:
            if self.is_dark(analog_pin, threshold):
                self.print(f"Dark condition reached")
                return True
            time.sleep(0.5)
        
        self.print(f"Timeout waiting for dark condition")
        return False
    
    def wait_for_bright(self, analog_pin, threshold=80, timeout=30):
        """
        Wait for light level to rise above threshold.
        
        Args:
            analog_pin (int): Arduino analog pin (0-5 for A0-A5)
            threshold (float): Light percentage threshold (default: 80%)
            timeout (float): Maximum time to wait in seconds (default: 30)
            
        Returns:
            bool: True if bright condition reached, False if timeout
            
        Example:
            if light.wait_for_bright(0, threshold=75, timeout=60):
                print("It got bright!")
        """
        start_time = time.time()
        
        while (time.time() - start_time) < timeout:
            if self.is_bright(analog_pin, threshold):
                self.print(f"Bright condition reached")
                return True
            time.sleep(0.5)
        
        self.print(f"Timeout waiting for bright condition")
        return False
    
    def monitor_light(self, analog_pin, duration=60, interval=1):
        """
        Monitor light levels continuously for a specified duration.
        
        Args:
            analog_pin (int): Arduino analog pin (0-5 for A0-A5)
            duration (float): Duration to monitor in seconds (default: 60)
            interval (float): Time between readings in seconds (default: 1)
            
        Returns:
            dict: Statistics including min, max, and average values
            
        Example:
            stats = light.monitor_light(0, duration=120, interval=2)
            print(f"Average light level: {stats['avg_percent']:.1f}%")
        """
        if not self._board or analog_pin not in self._sensors:
            self.eprint(f"Sensor on pin A{analog_pin} not configured")
            return {}
        
        raw_readings = []
        percent_readings = []
        start_time = time.time()
        
        self.print(f"Starting light monitoring for {duration} seconds...")
        
        while (time.time() - start_time) < duration:
            raw = self.read_light_level(analog_pin)
            percent = self.read_light_percent(analog_pin)
            
            if raw is not None and percent is not None:
                raw_readings.append(raw)
                percent_readings.append(percent)
                self.print(f"Light: {raw} raw ({percent:.1f}%)")
            
            time.sleep(interval)
        
        if not raw_readings:
            return {}
        
        stats = {
            "avg_raw": sum(raw_readings) / len(raw_readings),
            "min_raw": min(raw_readings),
            "max_raw": max(raw_readings),
            "avg_percent": sum(percent_readings) / len(percent_readings),
            "min_percent": min(percent_readings),
            "max_percent": max(percent_readings),
            "readings_count": len(raw_readings)
        }
        
        self.print(f"Monitoring complete:")
        self.print(f"  Raw: avg={stats['avg_raw']:.0f}, "
                   f"min={stats['min_raw']}, max={stats['max_raw']}")
        self.print(f"  Percent: avg={stats['avg_percent']:.1f}%, "
                   f"min={stats['min_percent']:.1f}%, max={stats['max_percent']:.1f}%")
        
        return stats
    
    def detect_light_change(self, analog_pin, threshold_percent=10, duration=5):
        """
        Detect significant change in light level over a time period.
        
        Args:
            analog_pin (int): Arduino analog pin (0-5 for A0-A5)
            threshold_percent (float): Minimum % change to detect (default: 10)
            duration (float): Time period to monitor in seconds (default: 5)
            
        Returns:
            dict: Change information or empty dict if no significant change
            
        Example:
            change = light.detect_light_change(0, threshold_percent=15)
            if change:
                print(f"Light changed by {change['change_percent']:.1f}%")
        """
        initial = self.read_light_percent(analog_pin)
        if initial is None:
            return {}
        
        time.sleep(duration)
        
        final = self.read_light_percent(analog_pin)
        if final is None:
            return {}
        
        change = abs(final - initial)
        
        if change >= threshold_percent:
            return {
                "changed": True,
                "initial_percent": initial,
                "final_percent": final,
                "change_percent": change,
                "direction": "increased" if final > initial else "decreased"
            }
        
        return {}
    
    def cleanup(self):
        """Clean up sensor configurations"""
        self._sensors.clear()
        self._last_readings.clear()
        self._callbacks.clear()
        self.print("Light sensor plugin cleanup completed")
