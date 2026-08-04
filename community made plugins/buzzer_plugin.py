"""
Buzzer Plugin for BrightOS

This plugin provides functions for controlling buzzers and speakers connected
to Arduino pins. Supports tone generation, melodies, and various sound patterns.

Example usage in a script:
    def main(plugins):
        buzzer = plugins.get("buzzer")
        if buzzer:
            # Setup buzzer on pin 8
            buzzer.setup_buzzer(8)
            
            # Play a tone
            buzzer.play_tone(8, 440, duration=1.0)  # A4 note
            
            # Play a melody
            buzzer.play_melody(8, "CDEFGABC")
            
            # Play alarm pattern
            buzzer.alarm(8, duration=5)
"""

from simple_plugin_loader.sample_plugin import SamplePlugin
import time


class Buzzer(SamplePlugin):
    """
    A plugin for controlling buzzers and playing tones.
    Requires a telemetrix board connection to function.
    """
    
    # Note frequencies in Hz
    NOTES = {
        'B0': 31, 'C1': 33, 'CS1': 35, 'D1': 37, 'DS1': 39, 'E1': 41, 'F1': 44, 'FS1': 46, 'G1': 49, 'GS1': 52, 'A1': 55, 'AS1': 58, 'B1': 62,
        'C2': 65, 'CS2': 69, 'D2': 73, 'DS2': 78, 'E2': 82, 'F2': 87, 'FS2': 93, 'G2': 98, 'GS2': 104, 'A2': 110, 'AS2': 117, 'B2': 123,
        'C3': 131, 'CS3': 139, 'D3': 147, 'DS3': 156, 'E3': 165, 'F3': 175, 'FS3': 185, 'G3': 196, 'GS3': 208, 'A3': 220, 'AS3': 233, 'B3': 247,
        'C4': 262, 'CS4': 277, 'D4': 294, 'DS4': 311, 'E4': 330, 'F4': 349, 'FS4': 370, 'G4': 392, 'GS4': 415, 'A4': 440, 'AS4': 466, 'B4': 494,
        'C5': 523, 'CS5': 554, 'D5': 587, 'DS5': 622, 'E5': 659, 'F5': 698, 'FS5': 740, 'G5': 784, 'GS5': 831, 'A5': 880, 'AS5': 932, 'B5': 988,
        'C6': 1047, 'CS6': 1109, 'D6': 1175, 'DS6': 1245, 'E6': 1319, 'F6': 1397, 'FS6': 1480, 'G6': 1568, 'GS6': 1661, 'A6': 1760, 'AS6': 1865, 'B6': 1976,
        'C7': 2093, 'CS7': 2217, 'D7': 2349, 'DS7': 2489, 'E7': 2637, 'F7': 2794, 'FS7': 2960, 'G7': 3136, 'GS7': 3322, 'A7': 3520, 'AS7': 3729, 'B7': 3951,
        'C8': 4186, 'CS8': 4435, 'D8': 4699, 'DS8': 4978
    }
    
    def __init__(self):
        """Initialize the buzzer plugin"""
        self._board = None
        self._buzzers = {}  # Track configured buzzers
        
    def set_board(self, board):
        """
        Set the telemetrix board instance for buzzer control
        
        Args:
            board: TelemetrixUnoR4WiFi board instance
        """
        self._board = board
        
    def setup_buzzer(self, pin):
        """
        Configure a pin for buzzer control.
        
        Args:
            pin (int): Arduino pin connected to buzzer
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            buzzer.setup_buzzer(8)
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        try:
            # Buzzers typically use PWM pins
            self._board.set_pin_mode_analog_output(pin)
            
            # Store buzzer configuration
            self._buzzers[pin] = {
                "active": False
            }
            
            self.print(f"Buzzer configured on pin {pin}")
            return True
            
        except Exception as e:
            self.eprint(f"Error setting up buzzer on pin {pin}: {e}")
            return False
    
    def play_tone(self, pin, frequency, duration=1.0):
        """
        Play a tone at a specific frequency.
        
        Args:
            pin (int): Arduino pin of the buzzer
            frequency (int): Frequency in Hz (31-4978)
            duration (float): Duration in seconds (default: 1.0)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            # Play middle C for 0.5 seconds
            buzzer.play_tone(8, 262, duration=0.5)
            
            # Play A4 (440 Hz) for 1 second
            buzzer.play_tone(8, 440, duration=1.0)
        """
        if not self._board:
            self.eprint("No board connected. Please connect to telemetrix first.")
            return False
            
        # Auto-setup if needed
        if pin not in self._buzzers:
            if not self.setup_buzzer(pin):
                return False
        
        try:
            # Check if board has tone support
            if hasattr(self._board, 'play_tone'):
                self._board.play_tone(pin, frequency, duration)
                self.print(f"Playing {frequency}Hz for {duration}s")
            else:
                # Fallback: Use PWM approximation
                # NOTE: This simplified PWM approach cannot generate specific frequencies.
                # The frequency parameter is ignored in this fallback mode.
                # For accurate tone generation, ensure your Arduino board has tone support.
                self.print(f"Warning: No tone support - frequency parameter ({frequency}Hz) ignored")
                self.print(f"Using basic PWM signal for {duration}s (no frequency control)")
                self._board.analog_write(pin, 128)  # 50% duty cycle
                time.sleep(duration)
                self._board.analog_write(pin, 0)
            
            return True
            
        except Exception as e:
            self.eprint(f"Error playing tone on pin {pin}: {e}")
            return False
    
    def play_note(self, pin, note, duration=0.5):
        """
        Play a musical note.
        
        Args:
            pin (int): Arduino pin of the buzzer
            note (str): Note name (e.g., "C4", "A4", "G5")
            duration (float): Duration in seconds (default: 0.5)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            buzzer.play_note(8, "C4", 0.5)  # Middle C
            buzzer.play_note(8, "A4", 1.0)  # A440
        """
        note = note.upper()
        if note not in self.NOTES:
            self.eprint(f"Unknown note: {note}")
            return False
        
        frequency = self.NOTES[note]
        return self.play_tone(pin, frequency, duration)
    
    def play_melody(self, pin, notes, tempo=120):
        """
        Play a melody from a string of notes.
        
        Args:
            pin (int): Arduino pin of the buzzer
            notes (str): String of note letters (e.g., "CDEFGABC")
            tempo (int): Tempo in BPM (default: 120)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            # Play C major scale
            buzzer.play_melody(8, "CDEFGABC")
            
            # Play faster
            buzzer.play_melody(8, "CDEFGABC", tempo=180)
        """
        # Calculate note duration based on tempo (quarter note)
        note_duration = 60.0 / tempo
        
        # Default octave
        octave = "4"
        
        for char in notes.upper():
            if char in "CDEFGAB":
                note_name = char + octave
                self.play_note(pin, note_name, note_duration)
                time.sleep(note_duration * 0.1)  # Small gap between notes
            elif char in "0123456789":
                octave = char
            elif char == " ":
                time.sleep(note_duration)  # Rest
        
        return True
    
    def beep(self, pin, times=1, duration=0.1, interval=0.1):
        """
        Make beeping sounds.
        
        Args:
            pin (int): Arduino pin of the buzzer
            times (int): Number of beeps (default: 1)
            duration (float): Duration of each beep in seconds (default: 0.1)
            interval (float): Time between beeps in seconds (default: 0.1)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            buzzer.beep(8)                    # Single beep
            buzzer.beep(8, times=3)           # Three beeps
            buzzer.beep(8, times=5, duration=0.2)  # Five longer beeps
        """
        for i in range(times):
            self.play_tone(pin, 1000, duration)  # 1kHz beep
            if i < times - 1:  # Don't wait after last beep
                time.sleep(interval)
        
        return True
    
    def alarm(self, pin, duration=5):
        """
        Play an alarm pattern (alternating high and low tones).
        
        Args:
            pin (int): Arduino pin of the buzzer
            duration (float): Total duration in seconds (default: 5)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            buzzer.alarm(8, duration=10)  # 10 second alarm
        """
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            self.play_tone(pin, 800, 0.2)  # High tone
            self.play_tone(pin, 400, 0.2)  # Low tone
        
        return True
    
    def siren(self, pin, duration=5):
        """
        Play a siren pattern (sweeping frequency).
        
        Args:
            pin (int): Arduino pin of the buzzer
            duration (float): Total duration in seconds (default: 5)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            buzzer.siren(8, duration=8)
        """
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            # Sweep up
            for freq in range(400, 1200, 50):
                self.play_tone(pin, freq, 0.05)
            # Sweep down
            for freq in range(1200, 400, -50):
                self.play_tone(pin, freq, 0.05)
        
        return True
    
    def chirp(self, pin):
        """
        Make a quick chirp sound.
        
        Args:
            pin (int): Arduino pin of the buzzer
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            buzzer.chirp(8)  # Quick chirp
        """
        for freq in range(1000, 2000, 200):
            self.play_tone(pin, freq, 0.02)
        return True
    
    def buzzer_morse(self, pin, message, wpm=15):
        """
        Play a message in Morse code.
        
        Args:
            pin (int): Arduino pin of the buzzer
            message (str): Message to send (letters and numbers)
            wpm (int): Words per minute (default: 15)
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            buzzer.buzzer_morse(8, "SOS")
            buzzer.buzzer_morse(8, "HELLO WORLD", wpm=20)
        """
        # Morse code dictionary
        morse_code = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
            '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.'
        }
        
        # Calculate timing based on WPM
        # Standard: PARIS (50 time units) = 1 word
        # Time unit = 1200ms / WPM
        unit_time = 1.2 / wpm
        dot_time = unit_time
        dash_time = unit_time * 3
        
        for char in message.upper():
            if char == ' ':
                time.sleep(unit_time * 7)  # Word space
            elif char in morse_code:
                code = morse_code[char]
                for symbol in code:
                    if symbol == '.':
                        self.play_tone(pin, 800, dot_time)
                    elif symbol == '-':
                        self.play_tone(pin, 800, dash_time)
                    time.sleep(unit_time)  # Symbol space
                time.sleep(unit_time * 3)  # Letter space
        
        return True
    
    def play_rtttl(self, pin, rtttl_string):
        """
        Play a melody in RTTTL (Ring Tone Text Transfer Language) format.
        Simplified version supporting basic RTTTL notation.
        
        Args:
            pin (int): Arduino pin of the buzzer
            rtttl_string (str): RTTTL format string
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            # Play a simple melody
            buzzer.play_rtttl(8, "Beep:d=4,o=5,b=120:c,d,e,f,g")
        """
        try:
            # Parse RTTTL (simplified)
            parts = rtttl_string.split(':')
            if len(parts) < 3:
                self.eprint("Invalid RTTTL format")
                return False
            
            # Parse defaults
            defaults = {}
            for item in parts[1].split(','):
                key, value = item.split('=')
                defaults[key] = value
            
            tempo = int(defaults.get('b', 120))
            default_octave = int(defaults.get('o', 5))
            note_duration = 60.0 / tempo
            
            # Parse and play notes
            notes = parts[2].split(',')
            for note in notes:
                # Very simplified parsing - just play the note
                note = note.strip()
                if note:
                    # Extract note letter and octave
                    note_letter = ''.join([c for c in note if c.isalpha()])
                    if note_letter:
                        note_name = note_letter.upper() + str(default_octave)
                        self.play_note(pin, note_name, note_duration)
            
            return True
            
        except Exception as e:
            self.eprint(f"Error playing RTTTL: {e}")
            return False
    
    def stop(self, pin):
        """
        Stop the buzzer (silence).
        
        Args:
            pin (int): Arduino pin of the buzzer
            
        Returns:
            bool: True if successful, False otherwise
            
        Example:
            buzzer.stop(8)
        """
        if not self._board or pin not in self._buzzers:
            return False
        
        try:
            self._board.analog_write(pin, 0)
            return True
        except Exception as e:
            self.eprint(f"Error stopping buzzer on pin {pin}: {e}")
            return False
    
    def cleanup(self):
        """Clean up buzzer configurations"""
        # Stop all buzzers
        for pin in list(self._buzzers.keys()):
            self.stop(pin)
        self._buzzers.clear()
        self.print("Buzzer plugin cleanup completed")
