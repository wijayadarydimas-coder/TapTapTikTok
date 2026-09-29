# main.py

import tkinter as tk

from tap_engine import TapEngine
from gui import TapGUI
from hotkeys import HotkeyManager


def main():

    # --------------------------------------------------------
    # TKINTER
    # --------------------------------------------------------

    root = tk.Tk()

    # --------------------------------------------------------
    # TAP ENGINE
    # --------------------------------------------------------

    engine = TapEngine()

    # --------------------------------------------------------
    # GUI
    # --------------------------------------------------------

    app = TapGUI(
        root,
        engine
    )

    # --------------------------------------------------------
    # HOTKEY
    # --------------------------------------------------------

    hotkeys = HotkeyManager(
        on_start_stop=engine.toggle,
        on_emergency_stop=engine.emergency_stop
    )

    hotkeys.start()

    # --------------------------------------------------------
    # CLOSE
    # --------------------------------------------------------

    def close_program():

        engine.stop()

        hotkeys.stop()

        root.destroy()

    root.protocol(
        "WM_DELETE_WINDOW",
        close_program
    )

    # --------------------------------------------------------
    # RUN
    # --------------------------------------------------------

    root.mainloop()


if __name__ == "__main__":
    main()