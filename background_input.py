# background_input.py
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
MK_LBUTTON = 0x0001


def make_lparam(x, y):
    # LOWORD = x, HIWORD = y
    return ((y & 0xFFFF) << 16) | (x & 0xFFFF)


class BackgroundMouse:
    """
    Experimental background mouse backend for Windows/Chromium.

    It does NOT move the physical cursor. It sends mouse messages directly
    to a window handle.

    Important:
    Modern Chromium pages may ignore synthetic background mouse messages.
    This class therefore cannot guarantee that a web page will treat them
    exactly like a physical mouse click.
    """

    def __init__(self, hwnd):
        self.hwnd = hwnd

    def set_target(self, hwnd):
        self.hwnd = hwnd

    def click(self, x, y):
        if not user32.IsWindow(self.hwnd):
            raise RuntimeError("Target window sudah tidak tersedia.")

        lp = make_lparam(int(x), int(y))

        # Send, rather than moving the real cursor.
        user32.PostMessageW(
            self.hwnd,
            WM_MOUSEMOVE,
            0,
            lp
        )

        user32.PostMessageW(
            self.hwnd,
            WM_LBUTTONDOWN,
            MK_LBUTTON,
            lp
        )

        user32.PostMessageW(
            self.hwnd,
            WM_LBUTTONUP,
            0,
            lp
        )
