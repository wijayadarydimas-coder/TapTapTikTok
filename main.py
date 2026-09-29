# main.py
import tkinter as tk

import config
from background_input import BackgroundMouse
from tap_engine import TapEngine
from hotkeys import HotkeyManager
from gui import TapGUI


def main():
    root = tk.Tk()

    # Akan diisi setelah user memilih window Opera.
    window_state = {
        "top_hwnd": None,
        "render_hwnd": None,
        "title": None,
    }

    # Default backend memakai HWND placeholder.
    backend = BackgroundMouse(0)

    engine = TapEngine(backend)

    app = TapGUI(
        root,
        engine,
        window_state,
    )

    hotkeys = HotkeyManager(
        on_start_stop=engine.toggle,
        on_emergency_stop=engine.emergency_stop,
    )
    hotkeys.start()

    def close():
        engine.stop()
        hotkeys.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close)
    root.mainloop()


if __name__ == "__main__":
    main()
