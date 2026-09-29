# gui.py

import tkinter as tk
from tkinter import ttk

from mouse_utils import get_mouse_position


class TapGUI:

    def __init__(self, root, engine):

        self.root = root
        self.engine = engine

        self.root.title("TikTok Tap Tool")
        self.root.geometry("450x480")
        self.root.resizable(False, False)

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = tk.Label(
            root,
            text="TIKTOK TAP TOOL",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=15)

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status_label = tk.Label(
            root,
            text="STATUS: READY",
            font=("Arial", 14, "bold"),
            foreground="blue"
        )

        self.status_label.pack()

        # ----------------------------------------------------
        # POSITION
        # ----------------------------------------------------

        position_frame = ttk.LabelFrame(
            root,
            text="Click Position"
        )

        position_frame.pack(
            padx=20,
            pady=15,
            fill="x"
        )

        tk.Label(
            position_frame,
            text="X:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=10
        )

        self.x_entry = tk.Entry(
            position_frame,
            width=10
        )

        self.x_entry.insert(
            0,
            str(engine.x)
        )

        self.x_entry.grid(
            row=0,
            column=1
        )

        tk.Label(
            position_frame,
            text="Y:"
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.y_entry = tk.Entry(
            position_frame,
            width=10
        )

        self.y_entry.insert(
            0,
            str(engine.y)
        )

        self.y_entry.grid(
            row=0,
            column=3
        )

        # ----------------------------------------------------
        # MOUSE POSITION BUTTON
        # ----------------------------------------------------

        tk.Button(
            position_frame,
            text="Ambil Posisi Mouse",
            command=self.get_position
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            pady=10
        )

        tk.Button(
            position_frame,
            text="Apply",
            command=self.apply_position
        ).grid(
            row=1,
            column=2,
            columnspan=2
        )

        self.coordinate_label = tk.Label(
            root,
            text=f"X={engine.x}   Y={engine.y}"
        )

        self.coordinate_label.pack()

        # ----------------------------------------------------
        # INFO
        # ----------------------------------------------------

        info_frame = ttk.LabelFrame(
            root,
            text="Tap Information"
        )

        info_frame.pack(
            padx=20,
            pady=15,
            fill="x"
        )

        tk.Label(
            info_frame,
            text="Pola:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )

        tk.Label(
            info_frame,
            text="100 TAP → 1 detik → ulangi"
        ).grid(
            row=0,
            column=1
        )

        self.tap_label = tk.Label(
            info_frame,
            text="Total Tap : 0"
        )

        self.tap_label.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=5
        )

        self.batch_label = tk.Label(
            info_frame,
            text="Batch : 0"
        )

        self.batch_label.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=5
        )

        # ----------------------------------------------------
        # BUTTON
        # ----------------------------------------------------

        button_frame = tk.Frame(root)

        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="START / STOP",
            width=15,
            height=2,
            command=self.engine.toggle
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        tk.Button(
            button_frame,
            text="EMERGENCY STOP",
            width=15,
            height=2,
            command=self.engine.emergency_stop
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Button(
            root,
            text="RESET",
            width=15,
            command=self.engine.reset
        ).pack()

        # ----------------------------------------------------
        # HOTKEY INFO
        # ----------------------------------------------------

        tk.Label(
            root,
            text="F6 = Start / Stop    |    F7 = Emergency Stop"
        ).pack(pady=15)

        # ----------------------------------------------------
        # CALLBACK
        # ----------------------------------------------------

        self.engine.set_status_callback(
            self.update_status
        )

    # ========================================================
    # GET POSITION
    # ========================================================

    def get_position(self):

        x, y = get_mouse_position()

        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, str(x))

        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(0, str(y))

        self.coordinate_label.config(
            text=f"X={x}   Y={y}"
        )

    # ========================================================
    # APPLY POSITION
    # ========================================================

    def apply_position(self):

        try:

            x = int(
                self.x_entry.get()
            )

            y = int(
                self.y_entry.get()
            )

            self.engine.set_position(
                x,
                y
            )

            self.coordinate_label.config(
                text=f"X={x}   Y={y}"
            )

        except ValueError:

            self.coordinate_label.config(
                text="Koordinat tidak valid!"
            )

    # ========================================================
    # STATUS CALLBACK
    # ========================================================

    def update_status(
        self,
        tap_count,
        batch_count,
        running,
        emergency_stopped
    ):

        # Tkinter harus di-update dari main thread.
        self.root.after(
            0,
            self._update_status_ui,
            tap_count,
            batch_count,
            running,
            emergency_stopped
        )

    # ========================================================
    # UPDATE UI
    # ========================================================

    def _update_status_ui(
        self,
        tap_count,
        batch_count,
        running,
        emergency_stopped
    ):

        if emergency_stopped:

            self.status_label.config(
                text="STATUS: EMERGENCY STOP",
                foreground="red"
            )

        elif running:

            self.status_label.config(
                text="STATUS: RUNNING",
                foreground="green"
            )

        else:

            self.status_label.config(
                text="STATUS: STOPPED",
                foreground="red"
            )

        self.tap_label.config(
            text=f"Total Tap : {tap_count:,}"
        )

        self.batch_label.config(
            text=f"Batch : {batch_count:,}"
        )