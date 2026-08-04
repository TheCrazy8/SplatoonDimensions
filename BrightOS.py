import math
import os
import datetime
import ast
import tkinter as tk
from tkinter import ttk
import threading
import queue
import sys
import importlib.util
import socket
try:
  from telemetrix_uno_r4.wifi.telemetrix_uno_r4_wifi import telemetrix_uno_r4_wifi as telemetrix_wifi
  TelemetrixUnoR4WiFi = telemetrix_wifi.TelemetrixUnoR4WiFi
except ImportError:
  TelemetrixUnoR4WiFi = None
from simple_plugin_loader import Loader
from contextlib import redirect_stdout, redirect_stderr
import io
import sv_ttk

# Configuration constants
ARDUINO_IP_ENV_VAR = "ARDUINO_IP_ADDRESS"
BROADCAST_PORT = 31335  # Must match DISCOVERY_PORT in Arduino code
DISCOVERY_TIMEOUT = 10  # seconds to wait for Arduino broadcast

def safe_listdir(path):
  try:
    return os.listdir(path)
  except FileNotFoundError:
    return []


def discover_arduino_ip():
  """
  Discover Arduino IP address by listening for UDP broadcasts.
  Returns the IP address as a string, or None if not found.
  Cross-platform implementation using socket.settimeout().
  Now accepts Arduino from any network configuration.
  """
  sock = None
  try:
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to the broadcast port on all interfaces
    sock.bind(('', BROADCAST_PORT))
    
    # Set timeout for cross-platform compatibility (Windows doesn't have select for sockets)
    sock.settimeout(DISCOVERY_TIMEOUT)
    
    # Wait for broadcast message
    try:
      data, addr = sock.recvfrom(1024)
      
      # Safely decode UTF-8 data
      try:
        message = data.decode('utf-8')
      except UnicodeDecodeError:
        # Try to decode with latin-1 as fallback
        try:
          message = data.decode('latin-1')
        except Exception:
          return None
      
      # Check if this is a BrightOS Arduino broadcast
      if message.startswith("BRIGHTOS_ARDUINO:"):
        ip_address = message.split(":", 1)[1].strip()
        
        # Basic validation - just check if it looks like an IP address
        # Accept any valid IPv4 format regardless of network range
        try:
          parts = ip_address.split('.')
          if len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts):
            # Valid IP format - return it
            return ip_address
        except (ValueError, AttributeError):
          pass
        
        # If basic validation fails, still try to use it if it's non-empty
        # This allows for edge cases or alternative formats
        if ip_address:
          return ip_address
          
    except socket.timeout:
      # No broadcast received within timeout
      return None
    
    return None
  except Exception:
    # Silently fail - error will be shown in GUI via calling function
    return None
  finally:
    # Ensure socket is always closed
    if sock:
      try:
        sock.close()
      except Exception:
        pass


def load_scripts(script_dir):
  """
  Load Python scripts as modules from the specified directory.
  Returns a dictionary with module names as keys and module objects as values.
  Only loads .py files that are not __init__.py.
  
  Note: Only load scripts from trusted directories as they will be executed.
  """
  scripts = {}
  
  if not os.path.exists(script_dir):
    return scripts
  
  # Get list of Python files
  try:
    files = [f for f in os.listdir(script_dir) 
             if f.endswith('.py') and f != '__init__.py']
  except (OSError, FileNotFoundError):
    return scripts
  
  # Import each script as a module
  for filename in files:
    filepath = os.path.join(script_dir, filename)
    module_name = filename[:-3]  # Remove .py extension
    
    try:
      # Load the module from file
      spec = importlib.util.spec_from_file_location(module_name, filepath)
      if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        scripts[module_name] = module
    except (ImportError, ModuleNotFoundError, SyntaxError) as e:
      print(f"Warning: Failed to load script '{filename}': {e}")
    except Exception as e:
      print(f"Warning: Unexpected error loading script '{filename}': {e}")
  
  return scripts

def get_brightos_dir():
    """Get the BrightOS directory path (cross-platform)"""
    userdir = os.path.expanduser("~")
    if sys.platform == "win32":
        return os.path.join(userdir, "AppData", "Local", "BrightOS")
    else:
        # For Linux/macOS, use a hidden directory in home
        return os.path.join(userdir, ".brightos")

brightos_dir = get_brightos_dir()
print(f"BrightOS directory: {brightos_dir}")

# Create directories with cross-platform paths
os.makedirs(os.path.join(brightos_dir, "Plugins"), exist_ok=True)
print("Directory 'Plugins' created/verified.")

os.makedirs(os.path.join(brightos_dir, "Scripts"), exist_ok=True)
print("Directory 'Scripts' created/verified.")

importlist_path = os.path.join(brightos_dir, "Importlist.txt")
if not os.path.exists(importlist_path):
    try:
        with open(importlist_path, 'w') as file:
            file.write("# BrightOS Import List\n")
        print("Created Importlist.txt")
    except Exception as e:
        print(f"Error creating Importlist.txt: {e}")
else:
    print("Importlist.txt already exists.")

plugin_dir = os.path.join(brightos_dir, "Plugins")
print(plugin_dir)
script_dir = os.path.join(brightos_dir, "Scripts")
print(script_dir)

# initialize the loader
loader = Loader()

# load your plugins
plugins = loader.load_plugins(plugin_dir)
# load scripts as modules (not using simple_plugin_loader since scripts are modules, not classes)
scripts = load_scripts(script_dir)
telemetrix_board = None
# Don't create the board at startup - let the user configure it through the GUI
plugins["telemetrix"] = telemetrix_board

def get_imports(path):
    with open(path, 'r') as fh:
        root = ast.parse(fh.read(), path)

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module
        else:
            continue

        for name in node.names:
            return(f"{name.name}")

def ChooseScript(plugins, scripts):
  output_queue = queue.Queue()
  running_thread = {"thread": None, "script": None}

  root = tk.Tk()
  root.title("BrightOS")
  
  # Set window icon (favicon)
  try:
    # Try to find the favicon in various locations
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Possible icon locations:
    # 1. When run from repository: docs/public/favicon.ico
    # 2. When run from launcher install: same directory as BrightOS.py
    # 3. When run from launcher install: ../../favicon.ico (up from install dir)
    possible_icon_paths = [
      os.path.join(script_dir, "docs", "public", "favicon.ico"),
      os.path.join(script_dir, "favicon.ico"),
      os.path.abspath(os.path.join(script_dir, "..", "..", "favicon.ico")),
    ]
    
    for icon_path in possible_icon_paths:
      if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
        break
  except Exception:
    # If icon setting fails, just continue without it
    pass

  ttk.Label(root, text="Select a script to run").pack(padx=10, pady=(10, 5))

  has_scripts = bool(scripts)

  if has_scripts:
    script_keys = list(scripts.keys())
    display_map = {str(k): k for k in script_keys}
    selected = tk.StringVar(value=str(script_keys[0]))
    options = list(display_map.keys())
  else:
    display_map = {}
    selected = tk.StringVar(value="No scripts")
    options = ["No scripts"]
    ttk.Label(root, text="No scripts found").pack(padx=10, pady=(0, 10))

  ttk.Combobox(root, textvariable=selected, values=options, state="readonly").pack(padx=10, pady=(0, 10))

  output = tk.Text(root, height=12, width=60, state=tk.DISABLED)
  output.pack(padx=10, pady=(0, 10))

  def append_output(msg):
    output.configure(state=tk.NORMAL)
    output.insert(tk.END, msg + "\n")
    output.see(tk.END)
    output.configure(state=tk.DISABLED)

  def poll_output():
    try:
      while True:
        msg = output_queue.get_nowait()
        append_output(msg)
    except queue.Empty:
      pass
    root.after(100, poll_output)

  def configure_telemetrix():
    if not TelemetrixUnoR4WiFi:
      append_output("Telemetrix library not available. Install telemetrix-uno-r4-wifi package.")
      return

    # Create a dialog window for Telemetrix configuration
    dialog = tk.Toplevel(root)
    dialog.title("Configure Telemetrix Connection")
    dialog.geometry("400x200")
    dialog.transient(root)
    dialog.grab_set()

    ttk.Label(dialog, text="Arduino Board IP Address:").pack(padx=10, pady=(20, 5))
    
    ip_entry = ttk.Entry(dialog, width=30)
    ip_entry.pack(padx=10, pady=(0, 10))
    
    # Pre-fill with environment variable if available
    env_ip = os.environ.get(ARDUINO_IP_ENV_VAR, "")
    if env_ip:
      ip_entry.insert(0, env_ip)
    
    status_label = ttk.Label(dialog, text="")
    status_label.pack(padx=10, pady=(10, 10))

    def connect():
      ip_address = ip_entry.get().strip()
      if not ip_address:
        status_label.config(text="Please enter an IP address")
        return

      status_label.config(text="Connecting...")
      dialog.update()

      try:
        # Shutdown existing connection if any
        if plugins["telemetrix"]:
          try:
            plugins["telemetrix"].shutdown()
          except Exception:
            pass

        # Create new connection
        new_board = TelemetrixUnoR4WiFi(transport_address=ip_address)
        plugins["telemetrix"] = new_board
        append_output(f"Telemetrix connected to {ip_address}")
        dialog.destroy()
      except Exception as exc:
        status_label.config(text=f"Connection failed: {exc}")
        append_output(f"Telemetrix connection failed: {exc}")

    def cancel():
      dialog.destroy()

    button_frame = ttk.Frame(dialog)
    button_frame.pack(padx=10, pady=(10, 20))
    
    ttk.Button(button_frame, text="Connect", command=connect).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=5)

  def disconnect_telemetrix():
    if plugins["telemetrix"]:
      try:
        plugins["telemetrix"].shutdown()
        plugins["telemetrix"] = None
        append_output("Telemetrix disconnected")
      except Exception as exc:
        append_output(f"Error disconnecting Telemetrix: {exc}")
    else:
      append_output("Telemetrix not connected")

  def auto_connect_telemetrix():
    """Automatically connect to Telemetrix using environment variable or network discovery"""
    if not TelemetrixUnoR4WiFi:
      return
    
    # Check if already connected
    if plugins["telemetrix"]:
      return
    
    # Try to get IP address from environment variable first
    arduino_ip = os.environ.get(ARDUINO_IP_ENV_VAR, "")
    
    # If not set, try to discover Arduino on the network
    if not arduino_ip:
      append_output("Searching for Arduino on network...")
      arduino_ip = discover_arduino_ip()
      
      if arduino_ip:
        append_output(f"Discovered Arduino at {arduino_ip}")
      else:
        append_output("No Arduino found on network. Use 'Configure Telemetrix' to connect manually.")
        return
    
    # Attempt connection
    try:
      append_output(f"Auto-connecting to Arduino at {arduino_ip}...")
      new_board = TelemetrixUnoR4WiFi(transport_address=arduino_ip)
      plugins["telemetrix"] = new_board
      append_output(f"Auto-connected to Telemetrix at {arduino_ip}")
    except Exception as exc:
      append_output(f"Auto-connection failed: {exc}")
      append_output("Use 'Configure Telemetrix' button to connect manually.")

  def run_selected():
    if running_thread["thread"] and running_thread["thread"].is_alive():
      append_output("A script is already running.")
      return

    key = display_map.get(selected.get())
    if key is None:
      append_output("No script selected.")
      return

    scripttorun = scripts.get(key)
    if not (scripttorun and hasattr(scripttorun, "main")):
      append_output("Selected script cannot be run.")
      return

    append_output(f"Running script: {key}")

    def target():
      class QueueWriter(io.StringIO):
        def write(self, s):
          super().write(s)
          if s and s != "\n":
            output_queue.put(s.rstrip("\n"))

      buf = QueueWriter()
      try:
        with redirect_stdout(buf), redirect_stderr(buf):
          scripttorun.main(plugins)
        output_queue.put("Script finished.")
      except Exception as exc:
        output_queue.put(f"Script error: {exc}")

    thread = threading.Thread(target=target, daemon=True)
    running_thread["thread"] = thread
    running_thread["script"] = scripttorun
    thread.start()

  def stop_running():
    thread = running_thread.get("thread")
    scripttorun = running_thread.get("script")
    if thread and thread.is_alive():
      if scripttorun and hasattr(scripttorun, "stop"):
        try:
          scripttorun.stop()
          append_output("Stop requested via script stop().")
        except Exception as exc:
          append_output(f"Stop failed: {exc}")
      else:
        append_output("Stop not supported for this script; ensure your script implements stop().")
    else:
      append_output("No running script to stop.")

  # Telemetrix configuration buttons
  telemetrix_frame = ttk.Frame(root)
  telemetrix_frame.pack(padx=10, pady=(0, 10))
  
  ttk.Button(telemetrix_frame, text="Configure Telemetrix", command=configure_telemetrix).pack(side=tk.LEFT, padx=5)
  ttk.Button(telemetrix_frame, text="Disconnect Telemetrix", command=disconnect_telemetrix).pack(side=tk.LEFT, padx=5)

  ttk.Button(root, text="Run", command=run_selected, state=tk.NORMAL if has_scripts else tk.DISABLED).pack(padx=10, pady=(0, 5))
  ttk.Button(root, text="Stop", command=stop_running).pack(padx=10, pady=(0, 10))

  append_output(f"Plugins loaded: {len(plugins)}, Scripts loaded: {len(scripts)}")
  
  # Attempt auto-connection if ARDUINO_IP_ADDRESS environment variable is set
  auto_connect_telemetrix()

  sv_ttk.use_dark_theme()
  poll_output()
  root.mainloop()


if __name__ == "__main__":
  ChooseScript(plugins, scripts)
