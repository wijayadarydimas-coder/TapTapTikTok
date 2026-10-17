# Background Tap Tool

Tool Windows/Python modular untuk menguji pengiriman synthetic mouse message ke window Opera/Chromium tanpa memindahkan physical cursor.

---

## 🛠️ Persiapan Lingkungan

Pilih salah satu metode instalasi dependencies berikut:

### Opsi A: Menggunakan Virtual Environment (Disarankan)

Gunakan virtual environment (`venv`) agar library proyek terisolasi dan tidak mengotori instalasi Python utama:

1. Buka PowerShell atau Command Prompt di folder proyek.
2. Buat virtual environment:
   ```powershell
   python -m venv venv
   ```
3. Aktifkan virtual environment:
   - **PowerShell:**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
     *(Jika muncul kendala Execution Policy pada PowerShell, jalankan: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` terlebih dahulu)*
   - **Command Prompt (CMD):**
     ```cmd
     venv\Scripts\activate.bat
     ```
4. Pasang library/dependencies yang dibutuhkan:
   ```powershell
   pip install -r requirements.txt
   ```

---

### Opsi B: Menggunakan Python Base (Langsung ke Sistem)

Jika tidak ingin membuat virtual environment, install package langsung ke Python global:

```powershell
python -m pip install -r requirements.txt
```

*(Atau via Python Launcher Windows: `py -m pip install -r requirements.txt`)*

---

## 🚀 Menjalankan Program

Setelah dependencies terpasang (dan venv aktif jika memilih Opsi A), jalankan aplikasi dengan:

```powershell
python main.py
```

*(Atau via launcher bawaan Windows: `py main.py`)*

---

## 🔁 Pola Kerja

```text
100 tap  ──>  Jeda 1 detik  ──>  100 tap  ──>  Jeda 1 detik  ──>  ...
```

---

## ⌨️ Hotkey

| Tombol | Fungsi |
| :--- | :--- |
| **F6** | Start / Stop |
| **F7** | Emergency Stop |

---

## ⚠️ Penting

- **Tanpa Pergeseran Kursor Fisik:** Mode ini tidak menggunakan `pyautogui`, sehingga kursor fisik pengguna tidak akan digerakkan sama sekali.
- **Batasan Chromium/Opera Modern:** Browser berbasis Chromium modern dapat mengabaikan synthetic message `WM_LBUTTONDOWN/UP` yang ditargetkan ke background window. Jika terjadi demikian, status program mungkin menandakan tap telah terkirim meskipun elemen web tidak merespons.
- **Deteksi Window:** Program mencari top-level window Opera berdasarkan keyword `TikTok`, kemudian mencoba mendeteksi child window `Chrome_RenderWidgetHostHWND`.
- **Koordinat:** Titik koordinat X/Y merupakan nilai relatif terhadap render window, bukan koordinat absolut layar monitor.
- **Kesesuaian Versi:** Jika Opera mengubah class atau struktur hierarchy window pada versi tertentu, penyesuaian mungkin diperlukan pada file `window_finder.py`.
