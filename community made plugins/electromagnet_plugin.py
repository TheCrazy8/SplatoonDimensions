"""
Electromagnet Plugin for BrightOS

This plugin provides functions for controlling electromagnets connected to Arduino pins.
Supports on/off control, PWM strength control, and timed operations.

Example usage in a script:
    def main(plugins):
        magnet = plugins.get("electromagnet")
        if magnet:
            # Turn on electromagnet on pin 7 at full strength
            magnet.activate(7, strength=100)
            
            # Turn on at 50% strength (PWM)
            magnet.activate(8, strength=50)
            
            # Turn off electromagnet
            magnet.deactivate(7)
            
            # Activate for a specific duration
            magnet.activate_timed(7, duration=5.0, strength=100)
"""

from simple_plugin_loader.sample_plugin import SamplePlugin
import time
import threading


class Electromagnet(SamplePlugin):
    """
    A plugin for controlling electromagnets with an Arduino board.
    Requires a telemetrix board connection to function.
    """
    
    def __init__(self):
        """Initialize the electromagnet controller plugin"""
        self._board = None
        self._magnet_pins = {}  # Track configured electromagnet pins
        self._timers = {}  # Track active timers for timed operations
        
    def set_board(self, board):
        """
        Set the telemetrix board instance for electromagnet control
        
        Args:
            board: TelemetrixUnoR4WiFi board instance
        """
        self._board = board
        
    def setup_magnet(self, pin, pwm=False):
        """
        Configure a pin for electromagnet control.
        
        Args:
            pin (int): Arduino pin number
            pwm (bool): Use PWM for strength control (default: False)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            magnet.setup_magnet(7)           # Digital on/off
            magnet.setup_magnet(9, pwm=True) # PWM strength control
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        try:
            if pwm:
                self._board.set_pin_mode_analog_output(pin)
            else:
                self._board.set_pin_mode_digital_output(pin)
            
            self._magnet_pins[pin] = {"pwm": pwm, "active": False, "strength": 0}
            self.print(f"Electromagnet configured on pin {pin} (PWM: {pwm})")
            return True
            
        except Exception as e:
            self.eprint(f"Error setting up electromagnet on pin {pin}: {e}")
            return False
    
    def activate(self, pin, strength=100):
        """
        Activate an electromagnet.
        
        Args:
            pin (int): Arduino pin number
            strength (int): Magnetic strength 0-100 (only for PWM pins, default: 100)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            magnet.activate(7)          # Full strength
            magnet.activate(9, 50)      # 50% strength (PWM only)
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        # Auto-setup pin if not configured
        if pin not in self._magnet_pins:
            # Always use PWM mode in auto-setup for maximum flexibility
            # This allows both full strength (100%) and variable strength (0-99%)
            if not self.setup_magnet(pin, pwm=True):
                return False
        
        if not 0 <= strength <= 100:
            self.eprint(f"Invalid strength {strength}. Must be between 0 and 100.")
            return False
            
        try:
            if self._magnet_pins[pin]["pwm"]:
                # PWM control for variable strength
                pwm_value = int((strength / 100.0) * 255)
                self._board.analog_write(pin, pwm_value)
                self.print(f"Electromagnet on pin {pin} activated at {strength}% strength")
            else:
                # Digital on/off control
                self._board.digital_write(pin, 1)
                self.print(f"Electromagnet on pin {pin} activated")
            
            self._magnet_pins[pin]["active"] = True
            self._magnet_pins[pin]["strength"] = strength
            return True
            
        except Exception as e:
            self.eprint(f"Error activating electromagnet on pin {pin}: {e}")
            return False
    
    def deactivate(self, pin):
        """
        Deactivate an electromagnet.
        
        Args:
            pin (int): Arduino pin number
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            magnet.deactivate(7)
        """
        if not self._board or pin not in self._magnet_pins:
            self.eprint(f"Electromagnet on pin {pin} not configured")
            return False
            
        try:
            # Cancel any active timer for this pin
            if pin in self._timers:
                self._timers[pin].cancel()
                del self._timers[pin]
            
            if self._magnet_pins[pin]["pwm"]:
                self._board.analog_write(pin, 0)
            else:
                self._board.digital_write(pin, 0)
            
            self._magnet_pins[pin]["active"] = False
            self._magnet_pins[pin]["strength"] = 0
            self.print(f"Electromagnet on pin {pin} deactivated")
            return True
            
        except Exception as e:
            self.eprint(f"Error deactivating electromagnet on pin {pin}: {e}")
            return False
    
    def activate_timed(self, pin, duration, strength=100):
        """
        Activate an electromagnet for a specific duration.
        
        Args:
            pin (int): Arduino pin number
            duration (float): Time in seconds to keep electromagnet active
            strength (int): Magnetic strength 0-100 (default: 100)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            # Activate for 5 seconds at full strength
            magnet.activate_timed(7, 5.0)
            
            # Activate for 3 seconds at 75% strength
            magnet.activate_timed(9, 3.0, 75)
        """
        if not self.activate(pin, strength):
            return False
        
        # Cancel any existing timer for this pin
        if pin in self._timers:
            self._timers[pin].cancel()
        
        # Create a new timer to deactivate after duration
        timer = threading.Timer(duration, self.deactivate, args=[pin])
        self._timers[pin] = timer
        timer.start()
        
        self.print(f"Electromagnet on pin {pin} will deactivate after {duration} seconds")
        return True
    
    def pulse(self, pin, on_time=0.5, off_time=0.5, cycles=3, strength=100):
        """
        Pulse an electromagnet on and off for a number of cycles.
        
        Args:
            pin (int): Arduino pin number
            on_time (float): Time in seconds electromagnet is on (default: 0.5)
            off_time (float): Time in seconds electromagnet is off (default: 0.5)
            cycles (int): Number of on/off cycles (default: 3)
            strength (int): Magnetic strength 0-100 (default: 100)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            # Pulse 5 times, 1 second on, 0.5 seconds off
            magnet.pulse(7, on_time=1.0, off_time=0.5, cycles=5)
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
        
        try:
            for i in range(cycles):
                self.print(f"Pulse {i+1}/{cycles}")
                self.activate(pin, strength)
                time.sleep(on_time)
                self.deactivate(pin)
                if i < cycles - 1:  # Don't wait after the last cycle
                    time.sleep(off_time)
            
            self.print(f"Pulse sequence completed on pin {pin}")
            return True
            
        except Exception as e:
            self.eprint(f"Error during pulse sequence on pin {pin}: {e}")
            return False
    
    def ramp_strength(self, pin, start=0, end=100, steps=20, delay=0.1):
        """
        Gradually ramp electromagnet strength from start to end.
        Only works with PWM pins.
        
        Args:
            pin (int): Arduino pin number (must be PWM)
            start (int): Starting strength 0-100 (default: 0)
            end (int): Ending strength 0-100 (default: 100)
            steps (int): Number of steps in ramp (default: 20)
            delay (float): Delay between steps in seconds (default: 0.1)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            # Gradually increase strength from 0 to 100%
            magnet.ramp_strength(9, 0, 100)
            
            # Gradually decrease strength from 100 to 0%
            magnet.ramp_strength(9, 100, 0)
        """
        if pin not in self._magnet_pins or not self._magnet_pins[pin]["pwm"]:
            self.eprint(f"Pin {pin} not configured for PWM control")
            return False
        
        try:
            step_size = (end - start) / steps
            for i in range(steps + 1):
                strength = int(start + (step_size * i))
                self.activate(pin, strength)
                time.sleep(delay)
            
            self.print(f"Strength ramp completed on pin {pin}")
            return True
            
        except Exception as e:
            self.eprint(f"Error during strength ramp on pin {pin}: {e}")
            return False
    
    def is_active(self, pin):
        """
        Check if an electromagnet is currently active.
        
        Args:
            pin (int): Arduino pin number
            
        Returns:
            bool: True if active, False otherwise
            
        Example:
            if magnet.is_active(7):
                print("Electromagnet is active")
        """
        if pin in self._magnet_pins:
            return self._magnet_pins[pin]["active"]
        return False
    
    def get_strength(self, pin):
        """
        Get the current strength setting of an electromagnet.
        
        Args:
            pin (int): Arduino pin number
            
        Returns:
            int: Current strength 0-100, or None if not configured
            
        Example:
            strength = magnet.get_strength(9)
            print(f"Current strength: {strength}%")
        """
        if pin in self._magnet_pins:
            return self._magnet_pins[pin]["strength"]
        return None
    
    def deactivate_all(self):
        """
        Deactivate all electromagnets.
        
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            magnet.deactivate_all()  # Emergency stop all electromagnets
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
        
        success = True
        for pin in list(self._magnet_pins.keys()):
            if not self.deactivate(pin):
                success = False
        
        if success:
            self.print("All electromagnets deactivated")
        return success
    
    def cleanup(self):
        """Clean up by deactivating all electromagnets and canceling timers"""
        # Cancel all active timers
        for timer in self._timers.values():
            timer.cancel()
        self._timers.clear()
        
        # Deactivate all electromagnets
        self.deactivate_all()
        self.print("Electromagnet plugin cleanup completed")
