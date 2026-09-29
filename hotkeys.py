# hotkeys.py

from pynput import keyboard


class HotkeyManager:

    def __init__(
        self,
        on_start_stop,
        on_emergency_stop
    ):

        self.on_start_stop = on_start_stop
        self.on_emergency_stop = on_emergency_stop

        self.listener = None

    # --------------------------------------------------------
    # KEY PRESS
    # --------------------------------------------------------

    def _on_press(self, key):

        try:

            if key == keyboard.Key.f6:

                self.on_start_stop()

            elif key == keyboard.Key.f7:

                self.on_emergency_stop()

        except Exception as error:

            print(
                f"Hotkey error: {error}"
            )

    # --------------------------------------------------------
    # START LISTENER
    # --------------------------------------------------------

    def start(self):

        self.listener = keyboard.Listener(
            on_press=self._on_press
        )

        self.listener.daemon = True

        self.listener.start()

    # --------------------------------------------------------
    # STOP LISTENER
    # --------------------------------------------------------

    def stop(self):

        if self.listener:

            self.listener.stop()