# tap_engine.py
import threading
import time
import config


class TapEngine:
    def __init__(self, backend, status_callback=None):
        self.backend = backend
        self.status_callback = status_callback

        self.running = False
        self.emergency_stopped = False

        self.tap_count = 0
        self.batch_count = 0

        self.x = config.DEFAULT_X
        self.y = config.DEFAULT_Y

        self.lock = threading.Lock()
        self.thread = None

    def set_status_callback(self, callback):
        self.status_callback = callback

    def set_position(self, x, y):
        with self.lock:
            self.x = int(x)
            self.y = int(y)
        self._notify()

    def _notify(self):
        if self.status_callback:
            self.status_callback(
                self.tap_count,
                self.batch_count,
                self.running,
                self.emergency_stopped,
            )

    def start(self):
        with self.lock:
            if self.emergency_stopped or self.running:
                return

            self.running = True
            self.thread = threading.Thread(
                target=self._worker,
                daemon=True,
            )
            self.thread.start()

        self._notify()

    def toggle(self):
        with self.lock:
            currently_running = self.running

        if currently_running:
            self.stop()
        else:
            self.start()

    def stop(self):
        with self.lock:
            self.running = False
        self._notify()

    def emergency_stop(self):
        with self.lock:
            self.running = False
            self.emergency_stopped = True
        self._notify()

    def reset(self):
        with self.lock:
            if self.running:
                return

            self.emergency_stopped = False
            self.tap_count = 0
            self.batch_count = 0

        self._notify()

    def _worker(self):
        while True:
            with self.lock:
                if not self.running or self.emergency_stopped:
                    break
                x, y = self.x, self.y

            for _ in range(config.TAPS_PER_BATCH):
                with self.lock:
                    if not self.running or self.emergency_stopped:
                        break
                    x, y = self.x, self.y

                try:
                    self.backend.click(x, y)
                except Exception as exc:
                    with self.lock:
                        self.running = False
                    if self.status_callback:
                        self.status_callback(
                            self.tap_count,
                            self.batch_count,
                            False,
                            self.emergency_stopped,
                            str(exc),
                        )
                    return

                with self.lock:
                    self.tap_count += 1

                self._notify()
                time.sleep(config.CLICK_INTERVAL)

            with self.lock:
                if not self.running or self.emergency_stopped:
                    break
                self.batch_count += 1

            self._notify()
            time.sleep(config.PAUSE_AFTER_BATCH)

        self._notify()
