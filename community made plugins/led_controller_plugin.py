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
