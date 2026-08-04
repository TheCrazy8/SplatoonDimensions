# Script Examples

Browse example scripts for BrightOS to help you get started. Each example includes code, description, and expected output. You can copy the code or try it directly in the [BrightOS Web Interface](/brightos-web).

## Beginner Examples

### Blink LED

Flash an LED on and off at regular intervals - the "Hello World" of Arduino programming.

**Hardware Required:**
- Arduino board
- LED (or use built-in LED on pin 13)
- 220Ω resistor (if using external LED)

**Expected Output:**
- LED turns on and off every second
- Console logs "LED ON" and "LED OFF" messages

```javascript
// Blink LED Example - Beginner
// Toggle an LED on/off every second

function main(plugins) {
  const board = plugins.get("telemetrix");
  
  if (!board) {
    console.error("Telemetrix not connected");
    return;
  }
  
  const LED_PIN = 13;
  let isOn = false;
  
  console.log("Starting LED blink on pin " + LED_PIN);
  
  // Note: arduino.write is a simplified example for demonstration
  // In actual implementation, use the board plugin methods
  // Toggle LED every second
  setInterval(() => {
    if (arduino.write) {
      const value = isOn ? 1 : 0;
      arduino.write(`digitalWrite(${LED_PIN}, ${value})\n`);
      console.log("LED " + (isOn ? "ON" : "OFF"));
      isOn = !isOn;
    }
  }, 1000);
}

function stop() {
  console.log("Blink stopped");
}
```

::: tip Try It Now
[Open in BrightOS Web](/brightos-web) - Copy the code above and load it as a script file.
:::

---

### Servo Sweep

Smoothly move a servo motor back and forth across its full range of motion.

**Hardware Required:**
- Arduino board
- Servo motor
- External power supply (recommended for most servos)

**Pin Configuration:**
- Servo signal: Pin 9
- Servo power: 5V (or external supply)
- Servo ground: GND

**Expected Output:**
- Servo sweeps from 0° to 180° and back
- Console displays current angle

```javascript
// Servo Sweep Example - Beginner
// Sweep a servo motor from 0 to 180 degrees

function main(plugins) {
  const board = plugins.get("telemetrix");
  const motor = plugins.get("motorcontroller");
  
  if (!motor || !board) {
    console.error("Required plugins not loaded");
    console.log("Make sure MotorController plugin is installed");
    return;
  }
  
  motor.set_board(board);
  
  const SERVO_PIN = 9;
  let angle = 0;
  let direction = 1;
  
  console.log("Starting servo sweep on pin " + SERVO_PIN);
  console.log("Servo will sweep from 0 to 180 degrees");
  
  const sweepInterval = setInterval(() => {
    motor.servo_control(SERVO_PIN, angle);
    console.log("Servo angle: " + angle + "°");
    
    angle += direction * 10;
    
    // Reverse direction at endpoints
    if (angle >= 180) {
      angle = 180;
      direction = -1;
      console.log("Reversing direction");
    } else if (angle <= 0) {
      angle = 0;
      direction = 1;
      console.log("Reversing direction");
    }
  }, 100);
}

function stop() {
  console.log("Servo sweep stopped");
  // Return servo to center position
  const motor = plugins.get("motorcontroller");
  if (motor) {
    motor.servo_control(9, 90);
  }
}
```

::: tip Try It Now
[Open in BrightOS Web](/brightos-web) - Requires MotorController plugin.
:::

---

### Simple Serial Output

Basic example showing how to send messages from Arduino to the console.

**Hardware Required:**
- Arduino board only

**Expected Output:**
- Messages appear in console every 2 seconds
- Shows timestamp with each message

```javascript
// Simple Serial Output - Beginner
// Send messages to console

function main(plugins) {
  const board = plugins.get("telemetrix");
  
  if (!board) {
    console.error("Telemetrix not connected");
    return;
  }
  
  let counter = 0;
  
  console.log("Serial output demo started");
  console.log("Sending messages every 2 seconds...");
  
  const outputInterval = setInterval(() => {
    counter++;
    console.log(`Message #${counter}: BrightOS is working!`);
    console.log(`Uptime: ${counter * 2} seconds`);
  }, 2000);
}

function stop() {
  console.log("Serial output stopped");
}
```

---

## Intermediate Examples

### Button Input Handler

Read button states and control an LED based on user input.

**Hardware Required:**
- Arduino board
- Push button
- LED and 220Ω resistor
- 10kΩ pull-down resistor for button

**Pin Configuration:**
- Button: Pin 2
- LED: Pin 13

**Expected Output:**
- LED turns on when button is pressed
- LED turns off when button is released
- Console logs button state changes

```javascript
// Button Input Handler - Intermediate
// Read button state and control LED

function main(plugins) {
  const board = plugins.get("telemetrix");
  
  if (!board) {
    console.error("Telemetrix not connected");
    return;
  }
  
  const BUTTON_PIN = 2;
  const LED_PIN = 13;
  let lastButtonState = false;
  
  console.log("Button input demo ready");
  console.log("Press button on pin " + BUTTON_PIN);
  console.log("LED on pin " + LED_PIN + " will respond");
  
  // Note: arduino.read and arduino.write are simplified for demonstration
  // In actual implementation, use board plugin callback methods
  // Poll button state
  const checkInterval = setInterval(() => {
    if (arduino.read) {
      arduino.read().then(data => {
        if (data) {
          const buttonPressed = data.includes("HIGH") || data.includes("1");
          
          // Only log when state changes
          if (buttonPressed !== lastButtonState) {
            lastButtonState = buttonPressed;
            
            if (buttonPressed) {
              console.log("Button PRESSED - LED ON");
              if (arduino.write) {
                arduino.write(`digitalWrite(${LED_PIN}, 1)\n`);
              }
            } else {
              console.log("Button RELEASED - LED OFF");
              if (arduino.write) {
                arduino.write(`digitalWrite(${LED_PIN}, 0)\n`);
              }
            }
          }
        }
      }).catch(err => {
        console.error("Read error:", err.message);
      });
    }
  }, 100);
}

function stop() {
  console.log("Button handler stopped");
  // Turn off LED
  if (arduino.write) {
    arduino.write("digitalWrite(13, 0)\n");
  }
}
```

::: tip Hardware Setup
Connect button between pin 2 and ground, with a 10kΩ pull-down resistor. Use internal pull-up if available.
:::

---

### Motor Speed Controller

Control DC motor speed with gradual acceleration and deceleration.

**Hardware Required:**
- Arduino board
- DC motor
- Motor driver (L298N or similar)
- External power supply for motor

**Pin Configuration:**
- Motor PWM: Pin 5
- Motor direction: Pin 4 (optional)

**Expected Output:**
- Motor accelerates from 0% to 100%
- Motor decelerates back to 0%
- Cycle repeats continuously
- Console displays current speed

```javascript
// Motor Speed Controller - Intermediate
// Control DC motor with gradual speed changes

function main(plugins) {
  const board = plugins.get("telemetrix");
  const motor = plugins.get("motorcontroller");
  
  if (!motor || !board) {
    console.error("Required plugins not loaded");
    return;
  }
  
  motor.set_board(board);
  
  const MOTOR_PIN = 5;
  const DIRECTION_PIN = 4;
  let speed = 0;
  let increasing = true;
  
  console.log("Motor speed controller started");
  console.log("Motor on pin " + MOTOR_PIN);
  console.log("Ramping speed from 0% to 100% and back");
  
  const controlInterval = setInterval(() => {
    // Set motor speed
    motor.dc_motor_control(MOTOR_PIN, speed, DIRECTION_PIN, true);
    console.log(`Motor speed: ${speed}%`);
    
    // Update speed
    if (increasing) {
      speed += 5;
      if (speed >= 100) {
        speed = 100;
        increasing = false;
        console.log("Max speed reached - decelerating");
      }
    } else {
      speed -= 5;
      if (speed <= 0) {
        speed = 0;
        increasing = true;
        console.log("Motor stopped - accelerating");
      }
    }
  }, 200);
}

function stop() {
  console.log("Motor controller stopped");
  const motor = plugins.get("motorcontroller");
  if (motor) {
    motor.stop_all();
  }
}
```

::: warning Power Requirements
DC motors require external power supply. Do not power motors directly from Arduino!
:::

---

### Multi-LED Pattern

Create light patterns with multiple LEDs in sequence.

**Hardware Required:**
- Arduino board
- 4-8 LEDs
- 220Ω resistors (one per LED)

**Pin Configuration:**
- LEDs on pins 8, 9, 10, 11, 12

**Expected Output:**
- LEDs light up in sequence (knight rider effect)
- Pattern repeats continuously
- Console shows which LED is active

```javascript
// Multi-LED Pattern - Intermediate
// Create moving light pattern with multiple LEDs

function main(plugins) {
  const board = plugins.get("telemetrix");
  
  if (!board) {
    console.error("Telemetrix not connected");
    return;
  }
  
  const LED_PINS = [8, 9, 10, 11, 12];
  let currentLED = 0;
  let direction = 1;
  
  console.log("LED pattern started");
  console.log("LEDs on pins: " + LED_PINS.join(", "));
  
  const patternInterval = setInterval(() => {
    // Turn off all LEDs
    LED_PINS.forEach(pin => {
      if (arduino.write) {
        arduino.write(`digitalWrite(${pin}, 0)\n`);
      }
    });
    
    // Turn on current LED
    if (arduino.write) {
      arduino.write(`digitalWrite(${LED_PINS[currentLED]}, 1)\n`);
    }
    console.log(`LED ${currentLED + 1}/${LED_PINS.length} ON (pin ${LED_PINS[currentLED]})`);
    
    // Move to next LED
    currentLED += direction;
    
    // Reverse direction at ends
    if (currentLED >= LED_PINS.length) {
      currentLED = LED_PINS.length - 2;
      direction = -1;
    } else if (currentLED < 0) {
      currentLED = 1;
      direction = 1;
    }
  }, 150);
}

function stop() {
  console.log("LED pattern stopped");
  // Turn off all LEDs
  const LED_PINS = [8, 9, 10, 11, 12];
  LED_PINS.forEach(pin => {
    if (arduino.write) {
      arduino.write(`digitalWrite(${pin}, 0)\n`);
    }
  });
}
```

---

## Advanced Examples

### Multi-Sensor Dashboard

Read data from multiple sensors and display in real-time dashboard format.

**Hardware Required:**
- Arduino board
- Temperature sensor (e.g., DHT11/DHT22)
- Light sensor (LDR)
- Distance sensor (HC-SR04)
- Various resistors

**Expected Output:**
- Continuous sensor readings every second
- Formatted dashboard display
- Alert messages when values exceed thresholds

```javascript
// Multi-Sensor Dashboard - Advanced
// Read and display data from multiple sensors

function main(plugins) {
  const board = plugins.get("telemetrix");
  
  if (!board) {
    console.error("Telemetrix not connected");
    return;
  }
  
  // Pin configuration
  const TEMP_PIN = 0;  // Analog pin A0
  const LIGHT_PIN = 1; // Analog pin A1
  const DISTANCE_TRIGGER = 7;
  const DISTANCE_ECHO = 8;
  
  let readingCount = 0;
  
  console.log("╔════════════════════════════════════╗");
  console.log("║   MULTI-SENSOR DASHBOARD v1.0      ║");
  console.log("╚════════════════════════════════════╝");
  console.log("");
  console.log("Initializing sensors...");
  console.log(`Temperature: Pin ${TEMP_PIN}`);
  console.log(`Light: Pin ${LIGHT_PIN}`);
  console.log(`Distance: Pins ${DISTANCE_TRIGGER}/${DISTANCE_ECHO}`);
  console.log("─".repeat(40));
  
  const dashboardInterval = setInterval(() => {
    readingCount++;
    
    // Simulate sensor readings (replace with actual sensor code)
    const temperature = (20 + Math.random() * 10).toFixed(1);
    const lightLevel = Math.floor(Math.random() * 100);
    const distance = (10 + Math.random() * 50).toFixed(1);
    const timestamp = new Date().toLocaleTimeString();
    
    // Display dashboard
    console.log(`\n[${timestamp}] Reading #${readingCount}`);
    console.log("┌────────────────────────────────────┐");
    console.log(`│ 🌡️  Temperature:  ${temperature}°C`.padEnd(37) + "│");
    console.log(`│ 💡 Light Level:  ${lightLevel}%`.padEnd(37) + "│");
    console.log(`│ 📏 Distance:     ${distance} cm`.padEnd(37) + "│");
    console.log("└────────────────────────────────────┘");
    
    // Alerts
    if (temperature > 28) {
      console.warn("⚠️  High temperature alert!");
    }
    if (lightLevel < 20) {
      console.warn("⚠️  Low light detected!");
    }
    if (distance < 15) {
      console.warn("⚠️  Object nearby!");
    }
    
    console.log("─".repeat(40));
  }, 2000);
}

function stop() {
  console.log("\nDashboard stopped");
  console.log("Thank you for using Multi-Sensor Dashboard!");
}
```

::: tip Advanced Usage
This example demonstrates formatting techniques, simulated data, and threshold alerts. Replace simulated readings with actual sensor code using the Telemetrix plugin methods.
:::

---

### Autonomous Robot Controller

Coordinate multiple motors and sensors for basic autonomous navigation.

**Hardware Required:**
- Arduino board
- 2x DC motors with motor driver
- 2x Servo motors
- Distance sensor (HC-SR04)
- Motor driver board (L298N)
- Chassis and wheels

**Expected Output:**
- Robot moves forward until obstacle detected
- Turns to avoid obstacle
- Resumes forward movement
- Console logs all decisions

```javascript
// Autonomous Robot Controller - Advanced
// Navigate and avoid obstacles

function main(plugins) {
  const board = plugins.get("telemetrix");
  const motor = plugins.get("motorcontroller");
  
  if (!motor || !board) {
    console.error("Required plugins not loaded");
    return;
  }
  
  motor.set_board(board);
  
  // Motor configuration
  const LEFT_MOTOR = 5;
  const RIGHT_MOTOR = 6;
  const SERVO_PIN = 9;
  const DISTANCE_THRESHOLD = 20; // cm
  
  let currentState = "INIT";
  let obstacleDetected = false;
  
  console.log("╔════════════════════════════════════╗");
  console.log("║   AUTONOMOUS ROBOT CONTROLLER      ║");
  console.log("╚════════════════════════════════════╝");
  console.log("");
  console.log("Initializing robot systems...");
  console.log("Motors: Pins " + LEFT_MOTOR + ", " + RIGHT_MOTOR);
  console.log("Servo scanner: Pin " + SERVO_PIN);
  console.log("─".repeat(40));
  
  // Center servo
  motor.servo_control(SERVO_PIN, 90);
  
  // Main control loop
  const controlInterval = setInterval(() => {
    // Simulate distance reading (replace with actual sensor)
    const distance = 30 + Math.random() * 50;
    
    if (distance < DISTANCE_THRESHOLD) {
      if (!obstacleDetected) {
        console.log("\n🚧 OBSTACLE DETECTED!");
        console.log(`Distance: ${distance.toFixed(1)} cm`);
        obstacleDetected = true;
        currentState = "AVOIDING";
        
        // Stop motors
        motor.stop_all();
        console.log("⏸️  Stopped");
        
        // Scan left and right
        setTimeout(() => {
          console.log("👀 Scanning left...");
          motor.servo_control(SERVO_PIN, 45);
          
          setTimeout(() => {
            console.log("👀 Scanning right...");
            motor.servo_control(SERVO_PIN, 135);
            
            setTimeout(() => {
              console.log("🔄 Turning right");
              motor.dc_motor_control(LEFT_MOTOR, 70);
              motor.dc_motor_control(RIGHT_MOTOR, 0);
              
              setTimeout(() => {
                motor.servo_control(SERVO_PIN, 90);
                obstacleDetected = false;
                currentState = "FORWARD";
                console.log("✅ Obstacle avoided\n");
              }, 1000);
            }, 500);
          }, 500);
        }, 500);
      }
    } else if (!obstacleDetected) {
      if (currentState !== "FORWARD") {
        console.log("⏩ Moving forward");
        currentState = "FORWARD";
      }
      // Move forward
      motor.dc_motor_control(LEFT_MOTOR, 60);
      motor.dc_motor_control(RIGHT_MOTOR, 60);
    }
  }, 250);
}

function stop() {
  console.log("\n🛑 Robot controller stopped");
  const motor = plugins.get("motorcontroller");
  if (motor) {
    motor.stop_all();
    motor.servo_control(9, 90);
  }
  console.log("All systems shutdown");
}
```

::: danger Safety Warning
Test autonomous robots in a safe, controlled environment. Ensure emergency stop is easily accessible. Never leave autonomous systems unattended.
:::

---

## Getting Started

### How to Use These Examples

1. **Copy the code** - Click the copy button in the top-right of any code block
2. **Save as file** - Save with a `.js` extension (e.g., `blink-led.js`)
3. **Load in BrightOS** - Use the [BrightOS Web Interface](/brightos-web) or desktop launcher
4. **Run the script** - Select the script and click "Run"

### Prerequisites

Most examples require:
- BrightOS installed and running
- Arduino board connected via USB
- Telemetrix plugin loaded (included with BrightOS)
- Some examples require the MotorController plugin

### Need Help?

- Check the [Development Guide](/development-guide) for detailed tutorials
- Visit the [Downloads](/downloads) page for plugins
- Review the [Build Guide](/BUILD) for setup instructions

---

## Contributing Examples

Have a great example to share? [Contribute on GitHub](https://github.com/TheCrazy8/Blaze-And-Company-Official)!

**Example Guidelines:**
- Clear, commented code
- Description of hardware requirements
- Expected output documented
- Tested on real hardware
- Follows BrightOS coding style
