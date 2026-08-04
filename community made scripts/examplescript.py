import time
import os
import pygame

# Configuration constants
ARDUINO_IP_ENV_VAR = "ARDUINO_IP_ADDRESS"

try:
  from telemetrix_uno_r4.wifi.telemetrix_uno_r4_wifi import telemetrix_uno_r4_wifi as telemetrix_wifi
  TelemetrixUnoR4WiFi = telemetrix_wifi.TelemetrixUnoR4WiFi
except ImportError:
  TelemetrixUnoR4WiFi = None

_board = None
_created_locally = False

userdir = home_dir = os.path.expanduser("~")

file_path = f"{userdir}\\AppData\\Local\\BrightOS\\Importlist.txt"
content_to_append = "\nPygame"

try:
    with open(file_path, "a") as file:
        file.write(content_to_append)
    print(f"Text appended to {file_path} successfully.")
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

def main(plugins):
  global _board, _created_locally
  _board = plugins.get("telemetrix") if isinstance(plugins, dict) else None
  _created_locally = False

  if _board is None and TelemetrixUnoR4WiFi:
    arduino_ip = os.environ.get(ARDUINO_IP_ENV_VAR)
    if arduino_ip:
      _board = TelemetrixUnoR4WiFi(transport_address=arduino_ip)
      _created_locally = True
    else:
      print(f"Cannot create Telemetrix board: {ARDUINO_IP_ENV_VAR} environment variable not set.")

  if not _board:
    print("Telemetrix board unavailable.")
    return

  _board.enable_scroll_message("example script")
  time.sleep(5)
  _board.disable_scroll_message()

  if _created_locally:
    _board.shutdown()


def stop():
  if _board:
    try:
      _board.disable_scroll_message()
    except Exception as exc:
      print(f"Could not disable scroll message: {exc}")
    if _created_locally:
      try:
        _board.shutdown()
      except Exception as exc:
        print(f"Could not shut down Telemetrix board: {exc}")
