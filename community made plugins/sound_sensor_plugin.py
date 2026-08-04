"""
Sound Sensor Plugin for BrightOS

This plugin provides functions for detecting sound levels using analog or digital
sound sensors (microphone modules) connected to Arduino pins.

Example usage in a script:
    def main(plugins):
        sound = plugins.get("soundsensor")
        if sound:
            # Setup analog sound sensor on A1
            sound.setup_analog(1)
            
            # Read sound level
            level = sound.read_sound_level(1)
            print(f"Sound level: {level}")
            
            # Check if loud
            if sound.is_loud(1, threshold=70):
                print("It's loud!")
            
            # Wait for loud sound
            if sound.wait_for_sound(1, threshold=60):
                print("Detected loud sound!")
"""

from simple_plugin_loader.sample_plugin import SamplePlugin
import time


class SoundSensor(SamplePlugin):
    """
    A plugin for detecting and measuring sound levels.
    Requires a telemetrix board connection to function.
    """
    
    def __init__(self):
        """Initialize the sound sensor plugin"""
        self._board = None
        self._sensors = {}  # Track configured sensors
        self._last_readings = {}  # Store last sound readings
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
    
    def _digital_callback(self, data):
        """Internal callback for digital readings"""
        pin = data[1]
        value = data[2]
        if pin in self._callbacks:
            self._last_readings[pin] = value
        
    def setup_analog(self, analog_pin):
        """
        Configure an analog pin for sound sensor reading.
        Use for analog microphone modules or sound level sensors.
        
        Args:
            analog_pin (int): Arduino analog pin (0-5 for A0-A5)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            sound.setup_analog(1)   # Setup on A1
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        try:
            # Configure analog input pin
            self._board.set_pin_mode_analog_input(analog_pin, callback=self._analog_callback)
            
            # Store sensor configuration
            self._sensors[analog_pin] = {
                "type": "analog",
                "baseline": None  # Will be calibrated on first read
            }
            self._last_readings[analog_pin] = 0
            self._callbacks[analog_pin] = True
            
            self.print(f"Analog sound sensor configured on pin A{analog_pin}")
            return True
            
        except Exception as e:
            self.eprint(f"Error setting up sound sensor on pin A{analog_pin}: {e}")
            return False
    
    def setup_digital(self, pin):
        """
        Configure a digital pin for sound detection.
        Use for digital sound sensor modules with threshold output.
        
        Args:
            pin (int): Arduino digital pin
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            sound.setup_digital(7)   # Setup on digital pin 7
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        try:
            # Configure digital input pin
            self._board.set_pin_mode_digital_input(pin, callback=self._digital_callback)
            
            # Store sensor configuration
            self._sensors[pin] = {
                "type": "digital"
            }
            self._last_readings[pin] = 0
            self._callbacks[pin] = True
            
            self.print(f"Digital sound sensor configured on pin {pin}")
            return True
            
        except Exception as e:
            self.eprint(f"Error setting up sound sensor on pin {pin}: {e}")
            return False
    
    def read_sound_level(self, pin):
        """
        Read sound level from analog sensor (0-1023).
        For digital sensors, returns 0 or 1.
        
        Args:
            pin (int): Arduino pin of the sensor
            
        Returns:
            int: Sound level value, or None if error
            
        Example:
            level = sound.read_sound_level(1)
            print(f"Sound: {level}")
        """
        if pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return None
        
        # Wait a moment for callback to update reading
        time.sleep(0.05)
        
        return self._last_readings.get(pin, 0)
    
    def read_sound_percent(self, pin):
        """
        Read sound level as percentage (0-100%).
        Only works with analog sensors.
        
        Args:
            pin (int): Arduino analog pin of the sensor
            
        Returns:
            float: Sound level percentage, or None if error
            
        Example:
            percent = sound.read_sound_percent(1)
            print(f"Sound: {percent:.1f}%")
        """
        if pin not in self._sensors or self._sensors[pin]["type"] != "analog":
            self.eprint(f"Analog sensor on pin A{pin} not configured")
            return None
        
        raw = self.read_sound_level(pin)
        if raw is None:
            return None
        
        return (raw / 1023.0) * 100.0
    
    def calibrate_baseline(self, pin, duration=2):
        """
        Calibrate the baseline (ambient) sound level.
        Call this in a quiet environment to set reference level.
        
        Args:
            pin (int): Arduino pin of the sensor
            duration (float): Duration to sample in seconds (default: 2)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            # Calibrate in quiet environment
            sound.calibrate_baseline(1, duration=3)
        """
        if pin not in self._sensors or self._sensors[pin]["type"] != "analog":
            self.eprint(f"Analog sensor on pin {pin} not configured")
            return False
        
        self.print("Calibrating baseline - please keep quiet...")
        
        readings = []
        end_time = time.time() + duration
        
        while time.time() < end_time:
            reading = self.read_sound_level(pin)
            if reading is not None:
                readings.append(reading)
            time.sleep(0.1)
        
        if not readings:
            self.eprint("Failed to collect calibration samples")
            return False
        
        baseline = sum(readings) / len(readings)
        self._sensors[pin]["baseline"] = baseline
        
        self.print(f"Baseline calibrated to {baseline:.1f}")
        return True
    
    def read_sound_above_baseline(self, pin):
        """
        Read sound level relative to calibrated baseline.
        Returns difference from baseline (0 if no baseline set).
        
        Args:
            pin (int): Arduino pin of the sensor
            
        Returns:
            float: Sound level above baseline, or None if error
            
        Example:
            # After calibrating baseline
            above = sound.read_sound_above_baseline(1)
            print(f"Sound above baseline: {above}")
        """
        if pin not in self._sensors:
            return None
        
        raw = self.read_sound_level(pin)
        if raw is None:
            return None
        
        baseline = self._sensors[pin].get("baseline", 0)
        if baseline is None:
            baseline = 0
        
        return max(0, raw - baseline)
    
    def is_loud(self, pin, threshold=70):
        """
        Check if sound level exceeds a threshold.
        For analog sensors, threshold is percentage (0-100).
        For digital sensors, checks if HIGH (1).
        
        Args:
            pin (int): Arduino pin of the sensor
            threshold (float): Threshold percentage for analog (default: 70)
            
        Returns:
            bool: True if loud, False otherwise
            
        Example:
            if sound.is_loud(1, threshold=65):
                print("Loud sound detected!")
        """
        if pin not in self._sensors:
            return False
        
        if self._sensors[pin]["type"] == "digital":
            # Digital sensor - check if HIGH
            return bool(self.read_sound_level(pin))
        else:
            # Analog sensor - check percentage
            percent = self.read_sound_percent(pin)
            if percent is None:
                return False
            return percent > threshold
    
    def wait_for_sound(self, pin, threshold=70, timeout=30):
        """
        Wait for sound level to exceed threshold.
        
        Args:
            pin (int): Arduino pin of the sensor
            threshold (float): Threshold percentage (default: 70)
            timeout (float): Maximum wait time in seconds (default: 30)
            
        Returns:
            bool: True if sound detected, False if timeout
            
        Example:
            if sound.wait_for_sound(1, threshold=60, timeout=60):
                print("Loud sound detected!")
        """
        if pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return False
        
        start_time = time.time()
        self.print(f"Waiting for sound above {threshold}%...")
        
        while (time.time() - start_time) < timeout:
            if self.is_loud(pin, threshold):
                self.print("Sound detected!")
                return True
            time.sleep(0.1)
        
        self.print("Timeout - no sound detected")
        return False
    
    def wait_for_quiet(self, pin, threshold=30, timeout=30):
        """
        Wait for sound level to drop below threshold.
        
        Args:
            pin (int): Arduino pin of the sensor
            threshold (float): Threshold percentage (default: 30)
            timeout (float): Maximum wait time in seconds (default: 30)
            
        Returns:
            bool: True if quiet, False if timeout
            
        Example:
            if sound.wait_for_quiet(1, threshold=25, timeout=60):
                print("It's quiet now")
        """
        if pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return False
        
        start_time = time.time()
        self.print(f"Waiting for sound below {threshold}%...")
        
        while (time.time() - start_time) < timeout:
            if not self.is_loud(pin, threshold):
                self.print("Quiet condition reached")
                return True
            time.sleep(0.1)
        
        self.print("Timeout - still loud")
        return False
    
    def monitor_sound(self, pin, duration=60, interval=0.5):
        """
        Monitor sound levels continuously for a specified duration.
        
        Args:
            pin (int): Arduino pin of the sensor
            duration (float): Duration to monitor in seconds (default: 60)
            interval (float): Time between readings in seconds (default: 0.5)
            
        Returns:
            dict: Statistics including min, max, and average values
            
        Example:
            stats = sound.monitor_sound(1, duration=120, interval=1)
            print(f"Average: {stats['avg_percent']:.1f}%")
            print(f"Peak: {stats['max_percent']:.1f}%")
        """
        if pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return {}
        
        is_analog = self._sensors[pin]["type"] == "analog"
        
        raw_readings = []
        percent_readings = []
        loud_count = 0
        start_time = time.time()
        
        self.print(f"Monitoring sound for {duration} seconds...")
        
        while (time.time() - start_time) < duration:
            raw = self.read_sound_level(pin)
            
            if raw is not None:
                raw_readings.append(raw)
                
                if is_analog:
                    percent = self.read_sound_percent(pin)
                    if percent is not None:
                        percent_readings.append(percent)
                        if percent > 70:  # Default loud threshold
                            loud_count += 1
                        self.print(f"Sound: {raw} raw ({percent:.1f}%)")
                else:
                    if raw:
                        loud_count += 1
                    self.print(f"Sound: {'HIGH' if raw else 'LOW'}")
            
            time.sleep(interval)
        
        if not raw_readings:
            return {}
        
        stats = {
            "readings_count": len(raw_readings),
            "loud_detections": loud_count
        }
        
        if is_analog and percent_readings:
            stats.update({
                "avg_raw": sum(raw_readings) / len(raw_readings),
                "min_raw": min(raw_readings),
                "max_raw": max(raw_readings),
                "avg_percent": sum(percent_readings) / len(percent_readings),
                "min_percent": min(percent_readings),
                "max_percent": max(percent_readings)
            })
            
            self.print(f"Monitoring complete:")
            self.print(f"  Avg: {stats['avg_percent']:.1f}%, "
                       f"Peak: {stats['max_percent']:.1f}%")
            self.print(f"  Loud detections: {loud_count}")
        else:
            self.print(f"Monitoring complete: {loud_count} loud detections")
        
        return stats
    
    def detect_clap(self, pin, sensitivity=80, timeout=5):
        """
        Detect a clap or sudden loud sound.
        
        Args:
            pin (int): Arduino pin of the sensor
            sensitivity (float): Detection threshold percentage (default: 80)
            timeout (float): Maximum wait time in seconds (default: 5)
            
        Returns:
            bool: True if clap detected, False if timeout
            
        Example:
            if sound.detect_clap(1, sensitivity=85):
                print("Clap detected - toggling light!")
        """
        return self.wait_for_sound(pin, threshold=sensitivity, timeout=timeout)
    
    def cleanup(self):
        """Clean up sensor configurations"""
        self._sensors.clear()
        self._last_readings.clear()
        self._callbacks.clear()
        self.print("Sound sensor plugin cleanup completed")
