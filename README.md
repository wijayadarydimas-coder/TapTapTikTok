# Background Tap Tool

Tool Windows/Python modular untuk menguji pengiriman synthetic mouse message
ke window Opera/Chromium tanpa memindahkan physical cursor.

## Install

```powershell
py -m pip install -r requirements.txt
```

## Jalankan

```powershell
py main.py
```

## Pola

100 tap -> jeda 1 detik -> 100 tap -> jeda 1 detik -> ...

## Hotkey

- F6 = Start/Stop
- F7 = Emergency Stop

## Penting

Mode ini tidak memakai `pyautogui`, jadi cursor fisik tidak dipindahkan.

Namun Chromium/Opera modern dapat mengabaikan synthetic `WM_LBUTTONDOWN/UP`
yang dikirim ke background window. Jika demikian, status program dapat
menunjukkan tap telah dikirim walaupun halaman web tidak bereaksi.

Program ini mencari top-level Opera window berdasarkan keyword `TikTok`, lalu
mencoba mencari child window `Chrome_RenderWidgetHostHWND`.

Koordinat X/Y adalah koordinat relatif terhadap render window, bukan koordinat
layar Windows.

Jika Opera menggunakan class/window structure berbeda pada versi tertentu,
`window_finder.py` mungkin perlu disesuaikan.
