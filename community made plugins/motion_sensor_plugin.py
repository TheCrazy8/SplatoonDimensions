"""
Motion Sensor Plugin for BrightOS

This plugin provides functions for detecting motion using PIR (Passive Infrared)
motion sensors connected to Arduino digital pins.

Example usage in a script:
    def main(plugins):
        motion = plugins.get("motionsensor")
        if motion:
            # Setup PIR sensor on pin 7
            motion.setup_pir(7)
            
            # Check for motion
            if motion.is_motion_detected(7):
                print("Motion detected!")
            
            # Wait for motion
            if motion.wait_for_motion(7, timeout=30):
                print("Someone moved!")
            
            # Monitor for a period
            detections = motion.monitor_motion(7, duration=60)
            print(f"Motion detected {detections} times")
"""

from simple_plugin_loader.sample_plugin import SamplePlugin
import time
import threading


class MotionSensor(SamplePlugin):
    """
    A plugin for detecting motion using PIR sensors.
    Requires a telemetrix board connection to function.
    """
    
    def __init__(self):
        """Initialize the motion sensor plugin"""
        self._board = None
        self._sensors = {}  # Track configured sensors
        self._motion_states = {}  # Track current motion states
        self._motion_counts = {}  # Track motion detection counts
        
    def set_board(self, board):
        """
        Set the telemetrix board instance for sensor control
        
        Args:
            board: TelemetrixUnoR4WiFi board instance
        """
        self._board = board
    
    def _motion_callback(self, data):
        """Internal callback for digital pin changes"""
        pin = data[1]
        value = data[2]
        if pin in self._sensors:
            self._motion_states[pin] = bool(value)
            if value:  # Motion detected (HIGH)
                self._motion_counts[pin] = self._motion_counts.get(pin, 0) + 1
        
    def setup_pir(self, pin):
        """
        Configure a digital pin for PIR motion sensor.
        
        Args:
            pin (int): Arduino digital pin connected to PIR sensor output
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            motion.setup_pir(7)   # PIR sensor on digital pin 7
            motion.setup_pir(12)  # PIR sensor on digital pin 12
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        try:
            # Configure digital input pin with callback
            self._board.set_pin_mode_digital_input(pin, callback=self._motion_callback)
            
            # Store sensor configuration
            self._sensors[pin] = {
                "type": "pir",
                "setup_time": time.time()
            }
            self._motion_states[pin] = False
            self._motion_counts[pin] = 0
            
            self.print(f"PIR motion sensor configured on pin {pin}")
            self.print("Note: PIR sensors typically need 30-60 seconds to stabilize after power-on")
            return True
            
        except Exception as e:
            self.eprint(f"Error setting up PIR sensor on pin {pin}: {e}")
            return False
    
    def is_motion_detected(self, pin):
        """
        Check if motion is currently detected.
        
        Args:
            pin (int): Arduino pin of the sensor
            
        Returns:
            bool: True if motion detected, False otherwise
            
        Example:
            if motion.is_motion_detected(7):
                print("Motion detected right now!")
        """
        if pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return False
        
        # Give a moment for callback to update
        time.sleep(0.05)
        
        return self._motion_states.get(pin, False)
    
    def wait_for_motion(self, pin, timeout=30):
        """
        Wait for motion to be detected.
        
        Args:
            pin (int): Arduino pin of the sensor
            timeout (float): Maximum time to wait in seconds (default: 30)
            
        Returns:
            bool: True if motion detected, False if timeout
            
        Example:
            if motion.wait_for_motion(7, timeout=60):
                print("Motion detected!")
            else:
                print("No motion detected within timeout")
        """
        if pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return False
        
        start_time = time.time()
        self.print(f"Waiting for motion on pin {pin}...")
        
        while (time.time() - start_time) < timeout:
            if self.is_motion_detected(pin):
                self.print("Motion detected!")
                return True
            time.sleep(0.1)
        
        self.print("Timeout - no motion detected")
        return False
    
    def wait_for_no_motion(self, pin, timeout=30):
        """
        Wait for motion to stop (sensor goes LOW).
        
        Args:
            pin (int): Arduino pin of the sensor
            timeout (float): Maximum time to wait in seconds (default: 30)
            
        Returns:
            bool: True if no motion detected, False if timeout
            
        Example:
            # Wait for area to be clear
            if motion.wait_for_no_motion(7, timeout=60):
                print("Area is clear!")
        """
        if pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return False
        
        start_time = time.time()
        self.print(f"Waiting for no motion on pin {pin}...")
        
        while (time.time() - start_time) < timeout:
            if not self.is_motion_detected(pin):
                self.print("No motion detected - area clear")
                return True
            time.sleep(0.1)
        
        self.print("Timeout - motion still detected")
        return False
    
    def monitor_motion(self, pin, duration=60):
        """
        Monitor motion for a specified duration and count detections.
        
        Args:
            pin (int): Arduino pin of the sensor
            duration (float): Duration to monitor in seconds (default: 60)
            
        Returns:
            int: Number of motion events detected
            
        Example:
            # Monitor for 5 minutes
            count = motion.monitor_motion(7, duration=300)
            print(f"Motion detected {count} times")
        """
        if pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return 0
        
        # Reset counter
        start_count = self._motion_counts.get(pin, 0)
        start_time = time.time()
        
        self.print(f"Monitoring motion for {duration} seconds...")
        
        last_state = False
        while (time.time() - start_time) < duration:
            current_state = self.is_motion_detected(pin)
            
            # Log state changes
            if current_state != last_state:
                if current_state:
                    self.print("Motion detected!")
                else:
                    self.print("Motion stopped")
                last_state = current_state
            
            time.sleep(0.2)
        
        total_detections = self._motion_counts.get(pin, 0) - start_count
        self.print(f"Monitoring complete: {total_detections} motion events detected")
        
        return total_detections
    
    def get_motion_count(self, pin):
        """
        Get the total number of motion events since sensor setup.
        
        Args:
            pin (int): Arduino pin of the sensor
            
        Returns:
            int: Total motion detection count
            
        Example:
            count = motion.get_motion_count(7)
            print(f"Total motion events: {count}")
        """
        return self._motion_counts.get(pin, 0)
    
    def reset_motion_count(self, pin):
        """
        Reset the motion event counter for a sensor.
        
        Args:
            pin (int): Arduino pin of the sensor
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            motion.reset_motion_count(7)
        """
        if pin in self._motion_counts:
            self._motion_counts[pin] = 0
            self.print(f"Motion counter reset for pin {pin}")
            return True
        return False
    
    def is_sensor_ready(self, pin, warmup_time=60):
        """
        Check if the PIR sensor has had enough time to stabilize.
        PIR sensors typically need 30-60 seconds after power-on.
        
        Args:
            pin (int): Arduino pin of the sensor
            warmup_time (float): Required warmup time in seconds (default: 60)
            
        Returns:
            bool: True if sensor is ready, False otherwise
            
        Example:
            if not motion.is_sensor_ready(7):
                print("Please wait for sensor to warm up...")
        """
        if pin not in self._sensors:
            return False
        
        setup_time = self._sensors[pin]["setup_time"]
        elapsed = time.time() - setup_time
        
        return elapsed >= warmup_time
    
    def wait_until_ready(self, pin, warmup_time=60):
        """
        Wait for the PIR sensor to complete its warmup period.
        
        Args:
            pin (int): Arduino pin of the sensor
            warmup_time (float): Required warmup time in seconds (default: 60)
            
        Returns:
            bool: True when ready, False if sensor not configured
            
        Example:
            motion.setup_pir(7)
            motion.wait_until_ready(7)  # Wait for sensor to be ready
            # Now safe to start detecting motion
        """
        if pin not in self._sensors:
            return False
        
        if self.is_sensor_ready(pin, warmup_time):
            self.print(f"Sensor on pin {pin} is ready")
            return True
        
        setup_time = self._sensors[pin]["setup_time"]
        elapsed = time.time() - setup_time
        remaining = warmup_time - elapsed
        
        if remaining > 0:
            self.print(f"Waiting {remaining:.1f} seconds for sensor to stabilize...")
            time.sleep(remaining)
        
        self.print(f"Sensor on pin {pin} is ready")
        return True
    
    def detect_presence(self, pin, check_duration=5, motion_threshold=2):
        """
        Check if someone is present in the area by monitoring motion over time.
        Returns True if motion is detected multiple times, suggesting presence.
        
        Args:
            pin (int): Arduino pin of the sensor
            check_duration (float): Duration to check in seconds (default: 5)
            motion_threshold (int): Minimum motion events to indicate presence (default: 2)
            
        Returns:
            bool: True if presence detected, False otherwise
            
        Example:
            if motion.detect_presence(7, check_duration=10):
                print("Someone is in the room")
        """
        if pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return False
        
        start_count = self._motion_counts.get(pin, 0)
        time.sleep(check_duration)
        end_count = self._motion_counts.get(pin, 0)
        
        motion_events = end_count - start_count
        
        return motion_events >= motion_threshold
    
    def cleanup(self):
        """Clean up sensor configurations"""
        self._sensors.clear()
        self._motion_states.clear()
        self._motion_counts.clear()
        self.print("Motion sensor plugin cleanup completed")
