# window_finder.py
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

EnumWindowsProc = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPARAM
)

def list_windows(keywords=None):
    """Return visible top-level windows whose title contains any keyword."""
    results = []
    keywords = [k.lower() for k in (keywords or [])]

    def callback(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True

        length = user32.GetWindowTextLengthW(hwnd)
        if length <= 0:
            return True

        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        title = buf.value

        if not keywords or any(k in title.lower() for k in keywords):
            results.append((hwnd, title))

        return True

    user32.EnumWindows(EnumWindowsProc(callback), 0)
    return results


def find_window_by_keywords(keywords):
    """Return first visible top-level window matching keywords."""
    matches = list_windows(keywords)
    return matches[0] if matches else None


def get_window_rect(hwnd):
    rect = wintypes.RECT()
    if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
        raise ctypes.WinError()
    return rect.left, rect.top, rect.right, rect.bottom


def get_client_rect_screen(hwnd):
    """Get client area rectangle in screen coordinates."""
    rect = wintypes.RECT()
    if not user32.GetClientRect(hwnd, ctypes.byref(rect)):
        raise ctypes.WinError()

    pt = wintypes.POINT(rect.left, rect.top)
    if not user32.ClientToScreen(hwnd, ctypes.byref(pt)):
        raise ctypes.WinError()

    width = rect.right - rect.left
    height = rect.bottom - rect.top
    return pt.x, pt.y, pt.x + width, pt.y + height


def find_render_child(hwnd):
    """
    Try to locate Chromium's render child window.
    Opera/Chromium class names can change, so several names are tried.
    """
    classes = [
        "Chrome_RenderWidgetHostHWND",
        "Chrome_RenderWidgetHostHWND1",
    ]

    for class_name in classes:
        child = user32.FindWindowExW(hwnd, 0, class_name, None)
        if child:
            return child

    return hwnd


def get_window_title(hwnd):
    length = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value
