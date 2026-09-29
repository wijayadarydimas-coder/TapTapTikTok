# gui.py
import tkinter as tk
from tkinter import ttk, messagebox

import config
from window_finder import list_windows, find_render_child, get_window_title


class TapGUI:
    def __init__(self, root, engine, window_state):
        self.root = root
        self.engine = engine
        self.window_state = window_state

        root.title("Background Tap Tool")
        root.geometry("560x540")
        root.resizable(False, False)

        tk.Label(
            root,
            text="BACKGROUND TAP TOOL",
            font=("Arial", 19, "bold"),
        ).pack(pady=14)

        self.status = tk.Label(
            root,
            text="STATUS: READY",
            font=("Arial", 12, "bold"),
        )
        self.status.pack()

        # Window selection
        wf = ttk.LabelFrame(root, text="Opera / Target Window")
        wf.pack(fill="x", padx=20, pady=12)

        self.window_combo = ttk.Combobox(
            wf,
            width=62,
            state="readonly",
        )
        self.window_combo.grid(
            row=0, column=0, padx=8, pady=8, columnspan=2
        )

        tk.Button(
            wf,
            text="Refresh",
            command=self.refresh_windows,
        ).grid(row=1, column=0, padx=8, pady=6, sticky="w")

        tk.Button(
            wf,
            text="Pilih Window",
            command=self.select_window,
        ).grid(row=1, column=1, padx=8, pady=6, sticky="e")

        self.window_info = tk.Label(
            wf,
            text="Belum ada window target.",
            anchor="w",
        )
        self.window_info.grid(
            row=2, column=0, columnspan=2,
            padx=8, pady=6, sticky="w"
        )

        # Position
        pf = ttk.LabelFrame(
            root,
            text="Target Coordinate - relatif ke render window",
        )
        pf.pack(fill="x", padx=20, pady=8)

        tk.Label(pf, text="X:").grid(row=0, column=0, padx=5, pady=8)
        self.x_entry = tk.Entry(pf, width=10)
        self.x_entry.insert(0, str(config.DEFAULT_X))
        self.x_entry.grid(row=0, column=1)

        tk.Label(pf, text="Y:").grid(row=0, column=2, padx=5)
        self.y_entry = tk.Entry(pf, width=10)
        self.y_entry.insert(0, str(config.DEFAULT_Y))
        self.y_entry.grid(row=0, column=3)

        tk.Button(
            pf,
            text="Apply",
            command=self.apply_position,
        ).grid(row=0, column=4, padx=10)

        # Counters
        inf = ttk.LabelFrame(root, text="Tap Information")
        inf.pack(fill="x", padx=20, pady=8)

        tk.Label(
            inf,
            text=f"Pola: {config.TAPS_PER_BATCH} tap → "
                 f"{config.PAUSE_AFTER_BATCH:g} detik → ulangi",
        ).pack(pady=5)

        self.tap_label = tk.Label(inf, text="Total Tap: 0")
        self.tap_label.pack()

        self.batch_label = tk.Label(inf, text="Batch: 0")
        self.batch_label.pack(pady=4)

        # Buttons
        bf = tk.Frame(root)
        bf.pack(pady=12)

        tk.Button(
            bf,
            text="START / STOP",
            width=18,
            height=2,
            command=self.engine.toggle,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            bf,
            text="EMERGENCY STOP",
            width=18,
            height=2,
            command=self.engine.emergency_stop,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            root,
            text="RESET",
            width=18,
            command=self.engine.reset,
        ).pack()

        tk.Label(
            root,
            text="F6 = Start/Stop    |    F7 = Emergency Stop",
        ).pack(pady=12)

        tk.Label(
            root,
            text=(
                "Catatan: mode background tidak memindahkan cursor.\n"
                "Chromium dapat menolak synthetic background mouse events."
            ),
            justify="center",
        ).pack()

        engine.set_status_callback(self.update_status)
        self.refresh_windows()

    def refresh_windows(self):
        matches = list_windows(config.WINDOW_TITLE_KEYWORDS)

        self.window_combo["values"] = [
            f"{hwnd} | {title}" for hwnd, title in matches
        ]

        if matches:
            self.window_combo.current(0)

    def select_window(self):
        value = self.window_combo.get()

        if not value:
            messagebox.showwarning(
                "Window",
                "Tidak ada window target yang dipilih.",
            )
            return

        hwnd = int(value.split("|", 1)[0].strip())
        title = get_window_title(hwnd)

        render = find_render_child(hwnd)

        self.window_state["top_hwnd"] = hwnd
        self.window_state["render_hwnd"] = render
        self.window_state["title"] = title

        self.engine.backend.set_target(render)

        self.window_info.config(
            text=f"Target: {title} | render HWND: {render}"
        )

    def apply_position(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            self.engine.set_position(x, y)
        except ValueError:
            messagebox.showerror(
                "Coordinate",
                "X dan Y harus berupa angka.",
            )

    def update_status(
        self,
        tap_count,
        batch_count,
        running,
        emergency_stopped,
        error_message=None,
    ):
        self.root.after(
            0,
            self._update_status_ui,
            tap_count,
            batch_count,
            running,
            emergency_stopped,
            error_message,
        )

    def _update_status_ui(
        self,
        tap_count,
        batch_count,
        running,
        emergency_stopped,
        error_message=None,
    ):
        if error_message:
            self.status.config(
                text=f"ERROR: {error_message}",
                foreground="red",
            )
        elif emergency_stopped:
            self.status.config(
                text="STATUS: EMERGENCY STOP",
                foreground="red",
            )
        elif running:
            self.status.config(
                text="STATUS: RUNNING",
                foreground="green",
            )
        else:
            self.status.config(
                text="STATUS: STOPPED",
                foreground="red",
            )

        self.tap_label.config(text=f"Total Tap: {tap_count:,}")
        self.batch_label.config(text=f"Batch: {batch_count:,}")
