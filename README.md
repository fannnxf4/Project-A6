# 🌹 Rose Diagram Generator

Aplikasi web interaktif untuk menghasilkan **Rose Diagram** dari data geologi struktural (strike dan dip). Aplikasi ini dibangun menggunakan Streamlit dan menyediakan visualisasi polar 360° yang menampilkan distribusi orientasi bidang dengan warna berdasarkan nilai dip.

## 📋 Deskripsi
Rose Diagram adalah visualisasi penting dalam geologi struktural untuk menganalisis orientasi bidang-bidang geologi seperti sesar, kekar, atau perlapisan batuan. Aplikasi ini memungkinkan pengguna untuk:
- Memasukkan data strike dan dip dengan format fleksibel
- Menghasilkan Rose Diagram 360° secara otomatis
- Melihat preview data dalam bentuk tabel
- Mengunduh data sebagai file CSV

## ✨ Fitur
- **Input Data Fleksibel**: Data dapat dimasukkan dengan dipisahkan koma atau baris baru
- **Validasi Data**: Memastikan data memenuhi syarat minimum (25 data) dan jumlah strike-dip sama
- **Visualisasi Interaktif**: Rose Diagram dengan colorbar yang menunjukkan rata-rata dip
- **Preview Data**: Tampilan tabel data sebelum dan sesudah pemrosesan
- **Export Data**: Unduh data sebagai  PNG atau file CSV untuk analisis lebih lanjut
- **User-Friendly Interface**: Antarmuka yang intuitif dan mudah digunaka

## 🛠️ Teknologi yang Digunaka
- **Streamlit**: Framework untuk membuat aplikasi web interaktif
- **NumPy**: Operasi matematika dan manipulasi array
- **Pandas**: Manipulasi dan analisis data
- **Matplotlib**: Visualisasi dan plotting diagram

## 📦 Instalasi

### Prasyarat

- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Langkah Instalasi
1. **Clone atau download repository ini*
2. **Install dependencies**
   ```bash

   pip install -r requirements.txt

   ```

   Atau install secara manual:

   ```bash

   pip install streamlit>=1.28.0

   pip install numpy>=1.24.0

   pip install pandas>=2.0.0

   pip install matplotlib>=3.7.0

   ```


## 🚀 Cara Menjalankan
1. **Jalankan aplikasi Streamlit**

   ```bash

   streamlit run app.py

   ```
2. **Buka browser**
   Aplikasi akan otomatis terbuka di browser default pada alamat:

   ```

   http://localhost:8518

   ```
   Jika tidak terbuka otomatis, salin URL yang ditampilkan di terminal dan buka di browser.

## 📖 Cara Penggunaan
### 1. Input Data Strike
Masukkan nilai-nilai strike (arah horizontal bidang) di text area pertama. Data dapat dipisahkan dengan:
- **Koma**: `185, 170, 173, 170, 198`

  **Baris baru**: 

```

  185

  170

  173

  17
  185
  170*:98


  ```

**Kombinasi*98`

**l*Catatan*n**: 
- Nilai strike biasanya dalam rentang 0-360 deraja- - Minimal diperlukan 25 data strike

### 2. Input Data Dip
Masukkan nilai-nilai dip (sudut kemiringan bidang) di text area kedua dengan format yang sa Inp Input Data2.  Input Data Dip Masukkan nilai-nilai dip (sudut kem ringan bidang) di text area kedua


**Catatan**:
- Nilai dip biasanya dalam rentang 0-90 derajat
- Minimal diperlukan 25 data dip
- Jumlah data dip harus sama dengan jumlah data strike

## 3. Masukan Nilai CSV (Opsional)

## 4. Generate Diagram
Klik tombol **"🚀 Generate Diagram"** untuk memproses data dan menghasilkan Rose Diagram.

### 5. Hasil
Setelah diagram dihasilkan, Anda akan melihat:

- **Rose Diagram 360°**: Visualisasi polar dengan bar chart

  - Panjang bar menunjukkan jumlah data dalam setiap bin arah (10° per bin)
  - Warna bar menunjukkan rata-rata nilai dip dalam setiap bin
  - Colorbar menunjukkan skala warna dip

- **Preview Data**: Tabel yang menampilkan semua data strike dan dip

- **Download CSV**: Tombol untuk mengunduh data sebagai fi
## 📊 Penjelasan Rose Diagram

### Komponen Diagram
1. **Sistem Koordinat Polar**
   - 0° berada di arah Utara (atas)
   - Rotasi searah jarum jam
   - Rentang penuh 360°

2. **Binning**
   - Data dibagi ke dalam bin dengan lebar 10°
   - Setiap bin mencakup rentang 10 derajat (misalnya: 0-10°, 10-20°, dst.)

3. **Panjang Bar**
   - Menunjukkan jumlah data yang masuk ke dalam setiap bin arah
   - Semakin panjang bar, semakin banyak data dalam arah terseb

4. **Warna Bar**
   - Menggunakan colormap "viridis" (hijau-biru-kuning)
   - Warna menunjukkan rata-rata nilai dip dalam setiap bin
   - Colorbar di samping diagram menunjukkan skala warna

### Algoritma Pemrosesan

1. **Normalisasi Strike**: Semua nilai strike dinormalisasi ke rentang 0-360°
2. **Folding**: Strike di-fold ke rentang 0-180° karena sifat bidirectional (strike 185° = strike 5°)
3. **Duplikasi**: Data diduplikasi untuk representasi 360° (setiap data muncul di azimuth dan azimuth+180°)
4. **Binning**: Data dikelompokkan ke dalam bin 10°
5. **Perhitungan**: Untuk setiap bin, dihitung jumlah data dan rata-rata dip
6. **Visualisasi**: Bar chart polar dengan warna berdasarkan dip

## ⚠️ Validasi Data

Aplikasi melakukan validasi berikut:
- ✅ Data strike tidak boleh kosong
- ✅ Data dip tidak boleh kosong
- ✅ Minimal 25 data untuk strike
- ✅ Minimal 25 data untuk dip
- ✅ Jumlah data strike harus sama dengan jumlah data d
Jika validasi gagal, pesan error akan ditampilkan dengan jelas.
## 📁 Struktur File

```

├── app.py                 # File utama aplikasi Streamlit

├── requirements.txt       # Daftar dependencies Python

└── README.md             # Dokumentasi proyek (file ini)

```

## 🔧 Konfigurasi
### Mengubah Ukuran Bin
Untuk mengubah lebar bin (default: 10°), edit variabel `bin_deg` di fungsi `generate_rose_diagram()`:

```python

bin_deg = 10  # Ubah nilai ini (misalnya: 5, 15, 20)

```

### Mengubah Colormap
Untuk mengubah colormap (default: 'viridis'), edit bagian berikut:


```python

color=plt.cm.viridis(dip_norm)  # Ganti 'viridis' dengan 'plasma', 'inferno', 'magma', dll.

```

Colormap yang tersedia: `viridis`, `plasma`, `inferno`, `magma`, `coolwarm`, dll.


## 🐛 Troubleshooting



### Error: "ModuleNotFoundError"



**Solusi**: Pastikan semua dependencies terinstall dengan benar:

```bash

pip install -r requirements.txt

```

### Error: "Data strike minimal 25"

**Solusi**: Pastikan Anda memasukkan minimal 25 data untuk strike dan dip.
### Diagram tidak muncul

**Solusi**: 

- Pastikan data valid (tidak ada error)
- Refresh halaman browser
- Cek console browser untuk error JavaScript


### Port sudah digunakan
**Solusi**: Gunakan port lain:

```bash

streamlit run app.py --server.port 8502

```


## 📝 Contoh Data

### Contoh Input Strike

```

185, 170, 173, 170, 198, 165, 180, 175, 190, 168,

172, 185, 178, 182, 175, 188, 170, 180, 185, 175,

190, 168, 172, 185, 178

```


### Contoh Input Dip

```

55, 67, 68, 75, 57, 60, 65, 70, 58, 62, 64, 66, 69, 72, 63, 61, 68, 65,70, 67, 59, 64, 66, 68, 71

```

## 🤝 Kontribusi
Kontribusi untuk meningkatkan aplikasi ini sangat diterima! Beberapa ide perbaikan:
- [ ] Statistik tambahan (mean, median, mode)
- [ ] Visualisasi 3D


## 📄 Lisensi
Proyek ini bebas digunakan untuk keperluan pendidikan dan penelitian.

## 👤 Author
Dibuat untuk keperluan analisis geologi struktural.



## 🙏 Acknowledgment
- Streamlit untuk framework yang powerfu
- Matplotlib untuk visualisasi yang berkualitas
- Komunitas geologi struktural untuk inspirasi

---

**Selamat menggunakan Rose Diagram Generator! 🌹**
Jika ada pertanyaan atau masalah, silakan buat issue di repository ini.
