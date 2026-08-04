"""
Motor Control Example Script for BrightOS

This script demonstrates how to use the MotorController plugin to control
different types of motors connected to an Arduino board.

Hardware Setup:
- Servo motor connected to pin 9
- DC motor connected to PWM pin 5 (with optional direction pin 4)

Before running:
1. Place motor_controller_plugin.py in the Plugins directory
2. Connect your Arduino board via Telemetrix
3. Wire your motors according to the pin configuration below
"""

import time

# Pin configuration - modify these according to your hardware setup
SERVO_PIN = 9           # Pin for servo motor (must support servo)
DC_MOTOR_PIN = 5        # PWM pin for DC motor speed control
DIRECTION_PIN = 4       # Pin for motor direction (optional, set to None if not used)

# Global variables for cleanup
_motor_controller = None


def main(plugins):
    """
    Main function to demonstrate motor control features.
    
    Args:
        plugins: Dictionary of loaded plugins, including telemetrix board and MotorController
    """
    global _motor_controller
    
    print("=" * 60)
    print("Motor Control Example Script")
    print("=" * 60)
    
    # Get the telemetrix board
    board = plugins.get("telemetrix")
    if not board:
        print("ERROR: Telemetrix board not connected.")
        print("Please configure and connect to Telemetrix first.")
        return
    
    # Get or create the MotorController plugin
    _motor_controller = plugins.get("motorcontroller")
    if not _motor_controller:
        print("ERROR: MotorController plugin not found.")
        print("Please ensure motor_controller_plugin.py is in the Plugins directory.")
        return
    
    # Initialize the motor controller with the board
    _motor_controller.set_board(board)
    print("Motor controller initialized with telemetrix board")
    print()
    
    # Run the motor control demos
    try:
        demo_servo_control()
        time.sleep(1)
        
        demo_dc_motor_control()
        time.sleep(1)
        
        demo_servo_sweep()
        time.sleep(1)
        
        demo_dc_motor_ramp()
        time.sleep(1)
        
        print("\n" + "=" * 60)
        print("All demonstrations completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
    except Exception as e:
        print(f"\nError during demonstration: {e}")
    finally:
        # Always stop all motors at the end
        if _motor_controller:
            print("\nStopping all motors...")
            _motor_controller.stop_all()


def demo_servo_control():
    """Demonstrate basic servo motor control"""
    print("\n--- Demo 1: Servo Control ---")
    print(f"Moving servo on pin {SERVO_PIN} to different positions...")
    
    positions = [0, 45, 90, 135, 180, 90]
    for angle in positions:
        print(f"  Position: {angle} degrees")
        _motor_controller.servo_control(SERVO_PIN, angle)
        time.sleep(1)
    
    # Check current position
    current_pos = _motor_controller.get_servo_position(SERVO_PIN)
    print(f"Current servo position: {current_pos} degrees")


def demo_dc_motor_control():
    """Demonstrate DC motor speed control"""
    print("\n--- Demo 2: DC Motor Speed Control ---")
    print(f"Controlling DC motor on pin {DC_MOTOR_PIN}...")
    
    speeds = [25, 50, 75, 100, 50, 0]
    for speed in speeds:
        print(f"  Speed: {speed}%")
        if DIRECTION_PIN:
            # Control with direction pin (forward)
            _motor_controller.dc_motor_control(DC_MOTOR_PIN, speed, 
                                              direction_pin=DIRECTION_PIN, 
                                              forward=True)
        else:
            # Control without direction pin
            _motor_controller.dc_motor_control(DC_MOTOR_PIN, speed)
        time.sleep(1.5)
    
    # Optional: Demonstrate reverse direction if direction pin is configured
    if DIRECTION_PIN:
        print("\n  Testing reverse direction...")
        for speed in [50, 100, 50, 0]:
            print(f"  Reverse speed: {speed}%")
            _motor_controller.dc_motor_control(DC_MOTOR_PIN, speed,
                                              direction_pin=DIRECTION_PIN,
                                              forward=False)
            time.sleep(1.5)


def demo_servo_sweep():
    """Demonstrate servo sweep function"""
    print("\n--- Demo 3: Servo Sweep ---")
    print(f"Sweeping servo on pin {SERVO_PIN} from 0 to 180 degrees and back...")
    
    _motor_controller.sweep_servo(SERVO_PIN, start_angle=0, end_angle=180, 
                                  step=2, delay=0.02)
    print("Servo sweep completed")


def demo_dc_motor_ramp():
    """Demonstrate DC motor speed ramping"""
    print("\n--- Demo 4: DC Motor Speed Ramping ---")
    print(f"Ramping DC motor on pin {DC_MOTOR_PIN}...")
    
    print("  Ramping up from 0% to 100%...")
    _motor_controller.ramp_dc_motor(DC_MOTOR_PIN, start_speed=0, end_speed=100,
                                   step=10, delay=0.2)
    
    time.sleep(1)
    
    print("  Ramping down from 100% to 0%...")
    _motor_controller.ramp_dc_motor(DC_MOTOR_PIN, start_speed=100, end_speed=0,
                                   step=10, delay=0.2)
    print("Motor ramp completed")


def stop():
    """
    Stop function called when user clicks the Stop button in BrightOS.
    Ensures all motors are stopped safely.
    """
    global _motor_controller
    print("\nStop requested - stopping all motors...")
    
    if _motor_controller:
        try:
            _motor_controller.stop_all()
            print("All motors stopped successfully")
        except Exception as e:
            print(f"Error stopping motors: {e}")
    else:
        print("Motor controller not initialized")


# Example of using the plugin functions individually:
"""
# In your own script, you can use the motor controller like this:

def main(plugins):
    # Get the motor controller and board
    # Note: Plugin keys are lowercase
    board = plugins.get("telemetrix")
    motor = plugins.get("motorcontroller")
    motor.set_board(board)
    
    # Control a servo
    motor.servo_control(9, 90)  # Move to 90 degrees
    
    # Control a DC motor
    motor.dc_motor_control(5, 75)  # Run at 75% speed
    
    # Stop a specific motor
    motor.stop_motor(5, "dc")
    
    # Stop all motors
    motor.stop_all()
"""
