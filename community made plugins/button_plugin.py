"""
Button/Switch Plugin for BrightOS

This plugin provides functions for reading button presses and switch states
from digital input devices connected to Arduino pins.

Example usage in a script:
    def main(plugins):
        button = plugins.get("button")
        if button:
            # Setup button on pin 2 with pull-up resistor
            button.setup_button(2, pull_up=True)
            
            # Check if button is pressed
            if button.is_pressed(2):
                print("Button is pressed!")
            
            # Wait for button press
            if button.wait_for_press(2):
                print("Button was pressed!")
            
            # Wait for release
            button.wait_for_release(2)
            print("Button released")
"""

from simple_plugin_loader.sample_plugin import SamplePlugin
import time


class Button(SamplePlugin):
    """
    A plugin for reading buttons and switches.
    Requires a telemetrix board connection to function.
    """
    
    def __init__(self):
        """Initialize the button plugin"""
        self._board = None
        self._buttons = {}  # Track configured buttons
        self._button_states = {}  # Track current button states
        self._press_counts = {}  # Track press counts
        
    def set_board(self, board):
        """
        Set the telemetrix board instance for button control
        
        Args:
            board: TelemetrixUnoR4WiFi board instance
        """
        self._board = board
    
    def _button_callback(self, data):
        """Internal callback for digital pin changes"""
        pin = data[1]
        value = data[2]
        if pin in self._buttons:
            pull_up = self._buttons[pin]["pull_up"]
            # With pull-up, pressed = LOW (0), released = HIGH (1)
            # Without pull-up, pressed = HIGH (1), released = LOW (0)
            is_pressed = (not value) if pull_up else bool(value)
            
            # Detect press event (transition from not pressed to pressed)
            if is_pressed and not self._button_states.get(pin, False):
                self._press_counts[pin] = self._press_counts.get(pin, 0) + 1
            
            self._button_states[pin] = is_pressed
        
    def setup_button(self, pin, pull_up=True):
        """
        Configure a digital pin for button input.
        
        Args:
            pin (int): Arduino digital pin connected to button
            pull_up (bool): Enable internal pull-up resistor (default: True)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            # Button with internal pull-up (common configuration)
            button.setup_button(2, pull_up=True)
            
            # Button with external pull-down resistor
            button.setup_button(3, pull_up=False)
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        try:
            # Configure digital input pin with callback
            if pull_up:
                self._board.set_pin_mode_digital_input_pullup(pin, callback=self._button_callback)
            else:
                self._board.set_pin_mode_digital_input(pin, callback=self._button_callback)
            
            # Store button configuration
            self._buttons[pin] = {
                "pull_up": pull_up
            }
            self._button_states[pin] = False
            self._press_counts[pin] = 0
            
            self.print(f"Button configured on pin {pin} (pull-up: {pull_up})")
            return True
            
        except Exception as e:
            self.eprint(f"Error setting up button on pin {pin}: {e}")
            return False
    
    def is_pressed(self, pin):
        """
        Check if button is currently pressed.
        
        Args:
            pin (int): Arduino pin of the button
            
        Returns:
            bool: True if pressed, False otherwise
            
        Example:
            if button.is_pressed(2):
                print("Button is down!")
        """
        if pin not in self._buttons:
            self.eprint(f"Button on pin {pin} not configured")
            return False
        
        # Give a moment for callback to update
        time.sleep(0.01)
        
        return self._button_states.get(pin, False)
    
    def is_released(self, pin):
        """
        Check if button is currently released (not pressed).
        
        Args:
            pin (int): Arduino pin of the button
            
        Returns:
            bool: True if released, False otherwise
            
        Example:
            if button.is_released(2):
                print("Button is up")
        """
        return not self.is_pressed(pin)
    
    def wait_for_press(self, pin, timeout=None):
        """
        Wait for button to be pressed.
        
        Args:
            pin (int): Arduino pin of the button
            timeout (float): Maximum wait time in seconds (default: None for infinite)
            
        Returns:
            bool: True if pressed, False if timeout
            
        Example:
            # Wait indefinitely
            button.wait_for_press(2)
            
            # Wait with timeout
            if button.wait_for_press(2, timeout=10):
                print("Pressed!")
            else:
                print("Timeout")
        """
        if pin not in self._buttons:
            self.eprint(f"Button on pin {pin} not configured")
            return False
        
        self.print(f"Waiting for button press on pin {pin}...")
        
        start_time = time.time()
        while True:
            if self.is_pressed(pin):
                self.print("Button pressed!")
                return True
            
            if timeout is not None and (time.time() - start_time) >= timeout:
                self.print("Timeout waiting for press")
                return False
            
            time.sleep(0.01)
    
    def wait_for_release(self, pin, timeout=None):
        """
        Wait for button to be released.
        
        Args:
            pin (int): Arduino pin of the button
            timeout (float): Maximum wait time in seconds (default: None for infinite)
            
        Returns:
            bool: True if released, False if timeout
            
        Example:
            button.wait_for_release(2)
            print("Button released")
        """
        if pin not in self._buttons:
            self.eprint(f"Button on pin {pin} not configured")
            return False
        
        self.print(f"Waiting for button release on pin {pin}...")
        
        start_time = time.time()
        while True:
            if self.is_released(pin):
                self.print("Button released!")
                return True
            
            if timeout is not None and (time.time() - start_time) >= timeout:
                self.print("Timeout waiting for release")
                return False
            
            time.sleep(0.01)
    
    def wait_for_click(self, pin, timeout=None):
        """
        Wait for a complete button click (press and release).
        
        Args:
            pin (int): Arduino pin of the button
            timeout (float): Maximum wait time in seconds (default: None for infinite)
            
        Returns:
            bool: True if clicked, False if timeout
            
        Example:
            if button.wait_for_click(2, timeout=10):
                print("Button clicked!")
        """
        # Wait for press
        if not self.wait_for_press(pin, timeout):
            return False
        
        # Calculate remaining timeout
        if timeout is not None:
            start_time = time.time()
        
        # Wait for release
        release_timeout = None
        if timeout is not None:
            elapsed = time.time() - start_time
            release_timeout = max(0, timeout - elapsed)
        
        if not self.wait_for_release(pin, release_timeout):
            return False
        
        self.print(f"Button click detected on pin {pin}")
        return True
    
    def get_press_count(self, pin):
        """
        Get the total number of button presses since setup.
        
        Args:
            pin (int): Arduino pin of the button
            
        Returns:
            int: Total press count
            
        Example:
            count = button.get_press_count(2)
            print(f"Pressed {count} times")
        """
        return self._press_counts.get(pin, 0)
    
    def reset_press_count(self, pin):
        """
        Reset the press counter for a button.
        
        Args:
            pin (int): Arduino pin of the button
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            button.reset_press_count(2)
        """
        if pin in self._press_counts:
            self._press_counts[pin] = 0
            self.print(f"Press counter reset for pin {pin}")
            return True
        return False
    
    def detect_long_press(self, pin, duration=2.0):
        """
        Detect if button is held down for a specified duration.
        
        Args:
            pin (int): Arduino pin of the button
            duration (float): Minimum hold time in seconds (default: 2.0)
            
        Returns:
            bool: True if long press detected, False otherwise
            
        Example:
            if button.detect_long_press(2, duration=3.0):
                print("Long press detected!")
        """
        if not self.is_pressed(pin):
            return False
        
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            if not self.is_pressed(pin):
                # Button was released before duration
                return False
            time.sleep(0.05)
        
        self.print(f"Long press detected on pin {pin}")
        return True
    
    def count_clicks(self, pin, timeout=3.0):
        """
        Count the number of button clicks within a timeout period.
        Useful for detecting double-clicks or multi-clicks.
        
        Args:
            pin (int): Arduino pin of the button
            timeout (float): Time window to count clicks in seconds (default: 3.0)
            
        Returns:
            int: Number of clicks detected
            
        Example:
            clicks = button.count_clicks(2, timeout=2.0)
            if clicks == 2:
                print("Double click!")
            elif clicks == 3:
                print("Triple click!")
        """
        if pin not in self._buttons:
            return 0
        
        click_count = 0
        start_time = time.time()
        
        # Wait for first press
        while (time.time() - start_time) < timeout:
            if self.is_pressed(pin):
                click_count += 1
                # Wait for release
                self.wait_for_release(pin, timeout=1.0)
                # Small delay to debounce
                time.sleep(0.1)
            else:
                time.sleep(0.01)
        
        if click_count > 0:
            self.print(f"Detected {click_count} clicks on pin {pin}")
        
        return click_count
    
    def read_switch_state(self, pin):
        """
        Read the current state of a toggle switch.
        Alias for is_pressed() for clarity when using switches vs buttons.
        
        Args:
            pin (int): Arduino pin of the switch
            
        Returns:
            bool: True if switch is ON, False if OFF
            
        Example:
            if button.read_switch_state(4):
                print("Switch is ON")
            else:
                print("Switch is OFF")
        """
        return self.is_pressed(pin)
    
    def wait_for_state_change(self, pin, timeout=None):
        """
        Wait for button/switch state to change (either press or release).
        
        Args:
            pin (int): Arduino pin of the button/switch
            timeout (float): Maximum wait time in seconds (default: None for infinite)
            
        Returns:
            str: "pressed" or "released" indicating the new state, or None if timeout
            
        Example:
            state = button.wait_for_state_change(2, timeout=10)
            if state:
                print(f"Button {state}")
        """
        if pin not in self._buttons:
            return None
        
        initial_state = self.is_pressed(pin)
        start_time = time.time()
        
        while True:
            current_state = self.is_pressed(pin)
            if current_state != initial_state:
                return "pressed" if current_state else "released"
            
            if timeout is not None and (time.time() - start_time) >= timeout:
                return None
            
            time.sleep(0.01)
    
    def cleanup(self):
        """Clean up button configurations"""
        self._buttons.clear()
        self._button_states.clear()
        self._press_counts.clear()
        self.print("Button plugin cleanup completed")
