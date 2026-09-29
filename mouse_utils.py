# mouse_utils.py

import pyautogui


def get_mouse_position():
    """
    Mengembalikan posisi cursor saat ini.

    Returns:
        tuple: (x, y)
    """

    return pyautogui.position()


def click_position(x, y):
    """
    Melakukan klik kiri pada koordinat tertentu.
    """

    pyautogui.click(x, y)