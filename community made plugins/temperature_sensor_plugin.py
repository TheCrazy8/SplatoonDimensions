"""
Temperature Sensor Plugin for BrightOS

This plugin provides functions for reading temperature and humidity from DHT sensors
(DHT11, DHT22/AM2302) connected to Arduino pins.

Example usage in a script:
    def main(plugins):
        temp = plugins.get("temperaturesensor")
        if temp:
            # Setup DHT22 sensor on pin 2
            temp.setup_dht(2, sensor_type="DHT22")
            
            # Read temperature in Celsius
            celsius = temp.read_temperature(2)
            print(f"Temperature: {celsius}°C")
            
            # Read temperature in Fahrenheit
            fahrenheit = temp.read_temperature_fahrenheit(2)
            print(f"Temperature: {fahrenheit}°F")
            
            # Read humidity
            humidity = temp.read_humidity(2)
            print(f"Humidity: {humidity}%")
            
            # Read both at once
            temp_c, hum = temp.read_temperature_humidity(2)
            print(f"{temp_c}°C, {hum}% humidity")
"""

from simple_plugin_loader.sample_plugin import SamplePlugin
import time
import math


class TemperatureSensor(SamplePlugin):
    """
    A plugin for reading temperature and humidity from DHT sensors.
    Requires a telemetrix board connection to function.
    """
    
    def __init__(self):
        """Initialize the temperature sensor plugin"""
        self._board = None
        self._sensors = {}  # Track configured sensors
        self._last_readings = {}  # Store last sensor readings
        
    def set_board(self, board):
        """
        Set the telemetrix board instance for sensor control
        
        Args:
            board: TelemetrixUnoR4WiFi board instance
        """
        self._board = board
        
    def setup_dht(self, pin, sensor_type="DHT22"):
        """
        Configure a DHT temperature/humidity sensor.
        
        Args:
            pin (int): Arduino pin connected to DHT sensor data pin
            sensor_type (str): Type of sensor - "DHT11" or "DHT22" (default: "DHT22")
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            temp.setup_dht(2, "DHT22")   # DHT22 on pin 2
            temp.setup_dht(4, "DHT11")   # DHT11 on pin 4
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
        
        sensor_type = sensor_type.upper()
        if sensor_type not in ["DHT11", "DHT22"]:
            self.eprint(f"Invalid sensor type '{sensor_type}'. Use 'DHT11' or 'DHT22'")
            return False
            
        try:
            # Configure DHT sensor pin
            # Note: Telemetrix typically has DHT support built-in
            # Check if board has DHT support
            if hasattr(self._board, 'set_pin_mode_dht'):
                # Use Telemetrix DHT support if available
                self._board.set_pin_mode_dht(pin)
            else:
                # Fallback: configure as digital input
                self._board.set_pin_mode_digital_input(pin)
            
            # Store sensor configuration
            self._sensors[pin] = {
                "type": sensor_type,
                "last_read_time": 0
            }
            self._last_readings[pin] = {
                "temperature": None,
                "humidity": None
            }
            
            self.print(f"{sensor_type} sensor configured on pin {pin}")
            return True
            
        except Exception as e:
            self.eprint(f"Error setting up {sensor_type} sensor on pin {pin}: {e}")
            return False
    
    def _read_dht_sensor(self, pin):
        """
        Internal method to read DHT sensor data.
        Returns tuple (temperature_celsius, humidity_percent) or (None, None) on error.
        
        NOTE: This is a placeholder implementation. For actual sensor readings,
        Telemetrix should have built-in DHT support with callbacks. Check your 
        Telemetrix documentation for the proper DHT implementation for your board.
        
        If your board doesn't support DHT mode, you'll need to implement
        DHT protocol timing on the Arduino side and read the results via callbacks.
        """
        if pin not in self._sensors:
            return None, None
        
        # DHT sensors need at least 2 seconds between readings
        current_time = time.time()
        last_read = self._sensors[pin]["last_read_time"]
        if current_time - last_read < 2.0:
            # Return cached value if too soon
            cached = self._last_readings[pin]
            return cached["temperature"], cached["humidity"]
        
        # NOTE: This implementation is incomplete and returns placeholder values.
        # For actual sensor readings, implement one of these approaches:
        # 1. Use Telemetrix's built-in DHT support with callbacks if available
        # 2. Create custom Arduino firmware that reads DHT data
        # 3. Use the DHT library on Arduino and send results via serial
        
        # Update last read time
        self._sensors[pin]["last_read_time"] = current_time
        
        # Return None to indicate no valid reading
        # Users should implement proper DHT support based on their hardware
        self.eprint("Warning: DHT sensor requires Telemetrix DHT support with callbacks.")
        self.eprint("Implementation options:")
        self.eprint("  1. Use board.set_pin_mode_dht() with callback if available")
        self.eprint("  2. Implement DHT protocol in Arduino firmware with DHT library")
        self.eprint("  3. Check Telemetrix documentation for DHT sensor support")
        return None, None
    
    def read_temperature(self, pin):
        """
        Read temperature from DHT sensor in Celsius.
        
        Args:
            pin (int): Arduino pin of the sensor
            
        Returns:
            float: Temperature in Celsius, or None if error
            
        Example:
            celsius = temp.read_temperature(2)
            if celsius is not None:
                print(f"Temperature: {celsius:.1f}°C")
        """
        if not self._board or pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return None
        
        temperature, _ = self._read_dht_sensor(pin)
        return temperature
    
    def read_temperature_fahrenheit(self, pin):
        """
        Read temperature from DHT sensor in Fahrenheit.
        
        Args:
            pin (int): Arduino pin of the sensor
            
        Returns:
            float: Temperature in Fahrenheit, or None if error
            
        Example:
            fahrenheit = temp.read_temperature_fahrenheit(2)
            if fahrenheit is not None:
                print(f"Temperature: {fahrenheit:.1f}°F")
        """
        celsius = self.read_temperature(pin)
        if celsius is not None:
            return (celsius * 9.0 / 5.0) + 32.0
        return None
    
    def read_humidity(self, pin):
        """
        Read humidity from DHT sensor as percentage.
        
        Args:
            pin (int): Arduino pin of the sensor
            
        Returns:
            float: Humidity percentage (0-100), or None if error
            
        Example:
            humidity = temp.read_humidity(2)
            if humidity is not None:
                print(f"Humidity: {humidity:.1f}%")
        """
        if not self._board or pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return None
        
        _, humidity = self._read_dht_sensor(pin)
        return humidity
    
    def read_temperature_humidity(self, pin):
        """
        Read both temperature and humidity from DHT sensor.
        
        Args:
            pin (int): Arduino pin of the sensor
            
        Returns:
            tuple: (temperature_celsius, humidity_percent) or (None, None) if error
            
        Example:
            temp_c, humidity = temp.read_temperature_humidity(2)
            if temp_c is not None:
                print(f"Temperature: {temp_c:.1f}°C, Humidity: {humidity:.1f}%")
        """
        if not self._board or pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return None, None
        
        return self._read_dht_sensor(pin)
    
    def calculate_heat_index(self, pin, use_fahrenheit=False):
        """
        Calculate heat index (feels-like temperature) based on temperature and humidity.
        
        Args:
            pin (int): Arduino pin of the sensor
            use_fahrenheit (bool): Return result in Fahrenheit (default: False for Celsius)
            
        Returns:
            float: Heat index in Celsius or Fahrenheit, or None if error
            
        Example:
            heat_index = temp.calculate_heat_index(2)
            print(f"Feels like: {heat_index:.1f}°C")
            
            # Get in Fahrenheit
            heat_index_f = temp.calculate_heat_index(2, use_fahrenheit=True)
            print(f"Feels like: {heat_index_f:.1f}°F")
        """
        temp_c, humidity = self.read_temperature_humidity(pin)
        
        if temp_c is None or humidity is None:
            return None
        
        # Convert to Fahrenheit for calculation (heat index formula uses Fahrenheit)
        temp_f = (temp_c * 9.0 / 5.0) + 32.0
        
        # Simplified heat index formula (valid for temp >= 80°F and humidity >= 40%)
        # Full formula from NOAA
        if temp_f >= 80 and humidity >= 40:
            hi = (-42.379 + 
                  2.04901523 * temp_f + 
                  10.14333127 * humidity - 
                  0.22475541 * temp_f * humidity - 
                  0.00683783 * temp_f * temp_f - 
                  0.05481717 * humidity * humidity + 
                  0.00122874 * temp_f * temp_f * humidity + 
                  0.00085282 * temp_f * humidity * humidity - 
                  0.00000199 * temp_f * temp_f * humidity * humidity)
        else:
            hi = temp_f  # No significant heat index at lower temps
        
        if use_fahrenheit:
            return hi
        else:
            return (hi - 32.0) * 5.0 / 9.0
    
    def calculate_dew_point(self, pin, use_fahrenheit=False):
        """
        Calculate dew point based on temperature and humidity.
        
        Args:
            pin (int): Arduino pin of the sensor
            use_fahrenheit (bool): Return result in Fahrenheit (default: False for Celsius)
            
        Returns:
            float: Dew point in Celsius or Fahrenheit, or None if error
            
        Example:
            dew_point = temp.calculate_dew_point(2)
            print(f"Dew point: {dew_point:.1f}°C")
        """
        temp_c, humidity = self.read_temperature_humidity(pin)
        
        if temp_c is None or humidity is None:
            return None
        
        # Validate humidity to prevent math domain error
        # Use small epsilon instead of 0 to avoid log(0)
        if humidity < 0.01 or humidity > 100:
            self.eprint(f"Invalid humidity value: {humidity}%")
            return None
        
        # Magnus formula for dew point calculation
        a = 17.27
        b = 237.7
        
        alpha = ((a * temp_c) / (b + temp_c)) + math.log(humidity / 100.0)
        dew_point_c = (b * alpha) / (a - alpha)
        
        if use_fahrenheit:
            return (dew_point_c * 9.0 / 5.0) + 32.0
        else:
            return dew_point_c
    
    def monitor_conditions(self, pin, duration=60, interval=5):
        """
        Monitor temperature and humidity continuously for a specified duration.
        
        Args:
            pin (int): Arduino pin of the sensor
            duration (float): Duration to monitor in seconds (default: 60)
            interval (float): Time between readings in seconds (default: 5, min: 2)
            
        Returns:
            dict: Statistics including min, max, and average values
            
        Example:
            # Monitor for 5 minutes, reading every 10 seconds
            stats = temp.monitor_conditions(2, duration=300, interval=10)
            print(f"Avg temp: {stats['avg_temp']:.1f}°C")
            print(f"Avg humidity: {stats['avg_humidity']:.1f}%")
        """
        if not self._board or pin not in self._sensors:
            self.eprint(f"Sensor on pin {pin} not configured")
            return {}
        
        # Ensure minimum interval for DHT sensors
        if interval < 2:
            interval = 2
            self.print("Interval adjusted to 2 seconds (minimum for DHT sensors)")
        
        temps = []
        humidities = []
        start_time = time.time()
        
        self.print(f"Starting environmental monitoring for {duration} seconds...")
        
        while (time.time() - start_time) < duration:
            temp_c, humidity = self.read_temperature_humidity(pin)
            if temp_c is not None and humidity is not None:
                temps.append(temp_c)
                humidities.append(humidity)
                self.print(f"Temp: {temp_c:.1f}°C, Humidity: {humidity:.1f}%")
            time.sleep(interval)
        
        if not temps:
            return {}
        
        stats = {
            "avg_temp": sum(temps) / len(temps),
            "min_temp": min(temps),
            "max_temp": max(temps),
            "avg_humidity": sum(humidities) / len(humidities),
            "min_humidity": min(humidities),
            "max_humidity": max(humidities),
            "readings_count": len(temps)
        }
        
        self.print(f"Monitoring complete:")
        self.print(f"  Temperature: avg={stats['avg_temp']:.1f}°C, "
                   f"min={stats['min_temp']:.1f}°C, max={stats['max_temp']:.1f}°C")
        self.print(f"  Humidity: avg={stats['avg_humidity']:.1f}%, "
                   f"min={stats['min_humidity']:.1f}%, max={stats['max_humidity']:.1f}%")
        
        return stats
    
    def is_comfortable(self, pin, temp_min=20, temp_max=26, humidity_min=30, humidity_max=60):
        """
        Check if current conditions are within comfortable ranges.
        
        Args:
            pin (int): Arduino pin of the sensor
            temp_min (float): Minimum comfortable temperature in Celsius (default: 20)
            temp_max (float): Maximum comfortable temperature in Celsius (default: 26)
            humidity_min (float): Minimum comfortable humidity % (default: 30)
            humidity_max (float): Maximum comfortable humidity % (default: 60)
            
        Returns:
            dict: Status with temperature and humidity comfort levels
            
        Example:
            status = temp.is_comfortable(2)
            if status['overall']:
                print("Conditions are comfortable")
            else:
                print(f"Temp OK: {status['temp_ok']}, Humidity OK: {status['humidity_ok']}")
        """
        temp_c, humidity = self.read_temperature_humidity(pin)
        
        if temp_c is None or humidity is None:
            return {"overall": False, "temp_ok": False, "humidity_ok": False}
        
        temp_ok = temp_min <= temp_c <= temp_max
        humidity_ok = humidity_min <= humidity <= humidity_max
        
        return {
            "overall": temp_ok and humidity_ok,
            "temp_ok": temp_ok,
            "humidity_ok": humidity_ok,
            "temperature": temp_c,
            "humidity": humidity
        }
    
    def cleanup(self):
        """Clean up sensor configurations"""
        self._sensors.clear()
        self._last_readings.clear()
        self.print("Temperature sensor plugin cleanup completed")
