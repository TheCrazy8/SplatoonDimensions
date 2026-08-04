"""
Motor Controller Plugin for BrightOS

This plugin provides functions for controlling different types of motors:
- Servo motors with precise rotation control
- DC motors with speed control using PWM
- Stepper motors (basic support)

Example usage in a script:
    def main(plugins):
        motor = plugins.get("MotorController")
        if motor:
            # Control a servo on pin 9 to 90 degrees
            motor.servo_control(9, 90)
            
            # Control a DC motor on pin 5 with 75% speed
            motor.dc_motor_control(5, 75)
            
            # Stop all motors
            motor.stop_all()
"""

from simple_plugin_loader.sample_plugin import SamplePlugin
import time


class MotorController(SamplePlugin):
    """
    A plugin for controlling various types of motors with an Arduino board.
    Requires a telemetrix board connection to function.
    """
    
    def __init__(self):
        """Initialize the motor controller plugin"""
        self._board = None
        self._servo_pins = {}  # Track servo pins and their current positions
        self._pwm_pins = {}    # Track PWM pins for DC motors
        
    def set_board(self, board):
        """
        Set the telemetrix board instance for motor control
        
        Args:
            board: TelemetrixUnoR4WiFi board instance
        """
        self._board = board
        
    def servo_control(self, pin, angle, min_pulse=544, max_pulse=2400):
        """
        Control a servo motor with precise rotation control.
        
        Args:
            pin (int): Arduino pin number where servo is connected (must support PWM)
            angle (int): Target angle in degrees (0-180)
            min_pulse (int): Minimum pulse width in microseconds (default: 544)
            max_pulse (int): Maximum pulse width in microseconds (default: 2400)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            motor.servo_control(9, 90)  # Move servo on pin 9 to 90 degrees
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        if not 0 <= angle <= 180:
            self.eprint(f"Invalid angle {angle}. Must be between 0 and 180 degrees.")
            return False
            
        try:
            # Set up servo pin if not already configured
            if pin not in self._servo_pins:
                self._board.set_pin_mode_servo(pin, min_pulse, max_pulse)
                self._servo_pins[pin] = angle
                self.print(f"Configured pin {pin} as servo")
            
            # Move servo to target angle
            self._board.servo_write(pin, angle)
            self._servo_pins[pin] = angle
            self.print(f"Servo on pin {pin} moved to {angle} degrees")
            return True
            
        except Exception as e:
            self.eprint(f"Error controlling servo on pin {pin}: {e}")
            return False
    
    def get_servo_position(self, pin):
        """
        Get the last known position of a servo motor.
        
        Args:
            pin (int): Arduino pin number of the servo
            
        Returns:
            int: Last known angle in degrees, or None if servo not configured
            
        Example:
            position = motor.get_servo_position(9)
            print(f"Servo at {position} degrees")
        """
        return self._servo_pins.get(pin)
    
    def dc_motor_control(self, pin, speed_percent, direction_pin=None, forward=True):
        """
        Control a DC motor with speed control using PWM.
        
        Args:
            pin (int): Arduino PWM pin for speed control
            speed_percent (int): Speed as percentage (0-100)
            direction_pin (int, optional): Pin for controlling direction (H-bridge)
            forward (bool): Direction - True for forward, False for reverse
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            # Single pin control (speed only)
            motor.dc_motor_control(5, 75)
            
            # With direction control
            motor.dc_motor_control(5, 75, direction_pin=4, forward=True)
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        if not 0 <= speed_percent <= 100:
            self.eprint(f"Invalid speed {speed_percent}. Must be between 0 and 100.")
            return False
            
        try:
            # Set up PWM pin if not already configured
            if pin not in self._pwm_pins:
                self._board.set_pin_mode_analog_output(pin)
                self._pwm_pins[pin] = 0
                self.print(f"Configured pin {pin} as PWM output")
            
            # Set up direction pin if provided
            if direction_pin is not None:
                self._board.set_pin_mode_digital_output(direction_pin)
                self._board.digital_write(direction_pin, 1 if forward else 0)
                self.print(f"Set direction pin {direction_pin} to {'forward' if forward else 'reverse'}")
            
            # Convert percentage to PWM value (0-255)
            pwm_value = int((speed_percent / 100.0) * 255)
            
            # Write PWM value to control speed
            self._board.analog_write(pin, pwm_value)
            self._pwm_pins[pin] = speed_percent
            self.print(f"DC motor on pin {pin} set to {speed_percent}% speed (PWM: {pwm_value})")
            return True
            
        except Exception as e:
            self.eprint(f"Error controlling DC motor on pin {pin}: {e}")
            return False
    
    def stop_motor(self, pin, motor_type="dc"):
        """
        Stop a specific motor by pin number.
        
        Args:
            pin (int): Arduino pin number
            motor_type (str): Type of motor - "dc" or "servo"
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            motor.stop_motor(5, "dc")     # Stop DC motor on pin 5
            motor.stop_motor(9, "servo")  # Stop servo on pin 9
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        try:
            if motor_type.lower() == "dc":
                if pin in self._pwm_pins:
                    self._board.analog_write(pin, 0)
                    self._pwm_pins[pin] = 0
                    self.print(f"Stopped DC motor on pin {pin}")
                    return True
            elif motor_type.lower() == "servo":
                if pin in self._servo_pins:
                    self._board.servo_detach(pin)
                    del self._servo_pins[pin]
                    self.print(f"Detached servo on pin {pin}")
                    return True
            
            self.eprint(f"No {motor_type} motor found on pin {pin}")
            return False
            
        except Exception as e:
            self.eprint(f"Error stopping motor on pin {pin}: {e}")
            return False
    
    def stop_all(self):
        """
        Stop all motors (both DC and servo).
        
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            motor.stop_all()  # Emergency stop all motors
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        success = True
        
        # Stop all DC motors
        for pin in list(self._pwm_pins.keys()):
            if not self.stop_motor(pin, "dc"):
                success = False
        
        # Stop all servos
        for pin in list(self._servo_pins.keys()):
            if not self.stop_motor(pin, "servo"):
                success = False
        
        if success:
            self.print("All motors stopped")
        return success
    
    def sweep_servo(self, pin, start_angle=0, end_angle=180, step=1, delay=0.015):
        """
        Sweep a servo motor back and forth between two angles.
        
        Args:
            pin (int): Arduino pin number where servo is connected
            start_angle (int): Starting angle in degrees (default: 0)
            end_angle (int): Ending angle in degrees (default: 180)
            step (int): Degrees to move per step (default: 1)
            delay (float): Delay in seconds between steps (default: 0.015)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            # Sweep servo from 0 to 180 degrees and back
            motor.sweep_servo(9)
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
        
        try:
            # Sweep forward
            for angle in range(start_angle, end_angle + 1, step):
                self.servo_control(pin, angle)
                time.sleep(delay)
            
            # Sweep backward
            for angle in range(end_angle, start_angle - 1, -step):
                self.servo_control(pin, angle)
                time.sleep(delay)
            
            self.print(f"Servo sweep completed on pin {pin}")
            return True
            
        except Exception as e:
            self.eprint(f"Error during servo sweep on pin {pin}: {e}")
            return False
    
    def ramp_dc_motor(self, pin, start_speed=0, end_speed=100, step=5, delay=0.1):
        """
        Gradually ramp a DC motor speed from start to end speed.
        
        Args:
            pin (int): Arduino PWM pin for the motor
            start_speed (int): Starting speed percentage (0-100)
            end_speed (int): Ending speed percentage (0-100)
            step (int): Speed increment per step (default: 5)
            delay (float): Delay in seconds between steps (default: 0.1)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            # Gradually speed up motor from 0 to 100%
            motor.ramp_dc_motor(5, 0, 100)
            
            # Gradually slow down motor from 100 to 0%
            motor.ramp_dc_motor(5, 100, 0)
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
        
        try:
            if start_speed < end_speed:
                # Ramping up
                for speed in range(start_speed, end_speed + 1, step):
                    self.dc_motor_control(pin, speed)
                    time.sleep(delay)
            else:
                # Ramping down
                for speed in range(start_speed, end_speed - 1, -step):
                    self.dc_motor_control(pin, speed)
                    time.sleep(delay)
            
            self.print(f"DC motor ramp completed on pin {pin}")
            return True
            
        except Exception as e:
            self.eprint(f"Error during motor ramp on pin {pin}: {e}")
            return False
