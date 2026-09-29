# hotkeys.py
from pynput import keyboard


class HotkeyManager:
    def __init__(self, on_start_stop, on_emergency_stop):
        self.on_start_stop = on_start_stop
        self.on_emergency_stop = on_emergency_stop
        self.listener = None

    def _on_press(self, key):
        if key == keyboard.Key.f6:
            self.on_start_stop()
        elif key == keyboard.Key.f7:
            self.on_emergency_stop()

    def start(self):
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.daemon = True
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
