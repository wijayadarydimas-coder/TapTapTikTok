# tap_engine.py

import threading
import time

import config
from mouse_utils import click_position


class TapEngine:

    def __init__(self, status_callback=None):
        self.running = False
        self.emergency_stopped = False

        self.tap_count = 0
        self.batch_count = 0

        self.x = config.DEFAULT_X
        self.y = config.DEFAULT_Y

        self.status_callback = status_callback

        self.thread = None

        self.lock = threading.Lock()

    # --------------------------------------------------------
    # SET CALLBACK
    # --------------------------------------------------------

    def set_status_callback(self, callback):
        self.status_callback = callback

    # --------------------------------------------------------
    # UPDATE STATUS
    # --------------------------------------------------------

    def _update_status(self):

        if self.status_callback:
            self.status_callback(
                self.tap_count,
                self.batch_count,
                self.running,
                self.emergency_stopped
            )

    # --------------------------------------------------------
    # SET POSITION
    # --------------------------------------------------------

    def set_position(self, x, y):

        with self.lock:
            self.x = int(x)
            self.y = int(y)

        self._update_status()

    # --------------------------------------------------------
    # START / STOP
    # --------------------------------------------------------

    def toggle(self):

        with self.lock:

            if self.emergency_stopped:
                return

            if self.running:

                self.running = False

            else:

                self.running = True

                if (
                    self.thread is None
                    or not self.thread.is_alive()
                ):

                    self.thread = threading.Thread(
                        target=self._worker,
                        daemon=True
                    )

                    self.thread.start()

        self._update_status()

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    def start(self):

        with self.lock:

            if self.emergency_stopped:
                return

            if self.running:
                return

            self.running = True

            self.thread = threading.Thread(
                target=self._worker,
                daemon=True
            )

            self.thread.start()

        self._update_status()

    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    def stop(self):

        with self.lock:
            self.running = False

        self._update_status()

    # --------------------------------------------------------
    # EMERGENCY STOP
    # --------------------------------------------------------

    def emergency_stop(self):

        with self.lock:

            self.running = False
            self.emergency_stopped = True

        self._update_status()

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    def reset(self):

        with self.lock:

            if self.running:
                return

            self.emergency_stopped = False

            self.tap_count = 0
            self.batch_count = 0

        self._update_status()

    # --------------------------------------------------------
    # WORKER
    # --------------------------------------------------------

    def _worker(self):

        while True:

            # ================================================
            # CHECK STATUS
            # ================================================

            with self.lock:

                if (
                    not self.running
                    or self.emergency_stopped
                ):
                    break

                x = self.x
                y = self.y

            # ================================================
            # 100 TAP
            # ================================================

            for _ in range(config.TAPS_PER_BATCH):

                with self.lock:

                    if (
                        not self.running
                        or self.emergency_stopped
                    ):
                        break

                    x = self.x
                    y = self.y

                # Tap
                click_position(x, y)

                with self.lock:
                    self.tap_count += 1

                self._update_status()

                # Interval antar tap
                time.sleep(config.CLICK_INTERVAL)

            # ================================================
            # CHECK LAGI
            # ================================================

            with self.lock:

                if (
                    not self.running
                    or self.emergency_stopped
                ):
                    break

                self.batch_count += 1

            self._update_status()

            # ================================================
            # JEDA 1 DETIK
            # ================================================

            time.sleep(config.PAUSE_AFTER_BATCH)

        self._update_status()