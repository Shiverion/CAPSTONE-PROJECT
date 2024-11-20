
# Sistem Pemesanan Lapangan Badminton

Sistem ini adalah aplikasi berbasis Python untuk membantu pengelolaan pemesanan lapangan badminton. Aplikasi ini memiliki fitur-fitur yang memungkinkan pengelola dan penyewa untuk mengatur jadwal, mengecek ketersediaan lapangan, dan mengelola pembayaran.

## Fitur Utama

1. **Pengelolaan Jadwal**
   - Tambah pemesanan lapangan.
   - Cek bentrokan jadwal.
   - Validasi jam operasional.

2. **Manajemen Pembayaran**
   - Status pembayaran: Pending, DP 50%, atau Lunas.
   - Opsi pembayaran DP atau penuh.

3. **Feedback dan Permintaan Perubahan**
   - Penyewa dapat memberikan feedback.
   - Penyewa dapat meminta penghapusan jadwal.

4. **Autentikasi Pengelola**
   - Hanya pengelola yang dapat mengakses menu pengelolaan.

5. **Validasi Tanggal dan Jam**
   - Pemesanan hanya dapat dilakukan minimal dua hari sebelumnya.
   - Waktu operasional divalidasi sesuai dengan hari (Weekday/Weekend).

6. **Visualisasi Jadwal**
   - Jadwal ditampilkan dalam format tabel yang mudah dibaca.

## Struktur Kode

- **Fungsi Utama**:
  - `main`: Mengarahkan pengguna ke menu pengelola atau penyewa.
  - `menu_pengelola`: Mengelola jadwal dan pembayaran.
  - `menu_penyewa`: Memungkinkan penyewa untuk membuat atau melihat pesanan mereka.

- **Fungsi Tambahan**:
  - `cek_bentrok`: Memastikan tidak ada jadwal yang tumpang tindih.
  - `cek_jam_operasional`: Memvalidasi waktu pemesanan sesuai jam operasional.
  - `lihat_daftar_pemesanan`: Menampilkan jadwal yang sudah ada.

## Instalasi

1. Pastikan Python 3.x sudah terinstal di komputer Anda.
2. Instal dependensi dengan perintah berikut:
   ```bash
   pip install tabulate
   ```

3. Jalankan program dengan perintah:
   ```bash
   python CAPPSTONE_PROJECT_1.py
   ```

## Penggunaan

1. **Pilih Peran**:
   - Pengelola atau Penyewa.
2. **Autentikasi Pengelola**:
   - Masukkan username dan password untuk mengakses fitur pengelola.
3. **Tambahkan Pemesanan**:
   - Isi detail penyewaan: nama, tanggal, jam mulai, durasi, dan nomor lapangan.
4. **Feedback dan Perubahan**:
   - Masukkan nama penyewa untuk memberikan masukan atau meminta perubahan.

## Teknologi yang Digunakan

- **Bahasa Pemrograman**: Python
- **Pustaka Tambahan**:
  - `tabulate`: Untuk menampilkan jadwal dalam format tabel.
  - `datetime`: Untuk manipulasi tanggal dan waktu.
  - `re`: Untuk validasi input nama.

## Kontributor

- **Nama**: Muhammad Iqbal Hilmy Izzulhaq
- **Peran**: Developer

## Lisensi

Proyek ini dirilis di bawah lisensi MIT. Silakan gunakan dan modifikasi sesuai kebutuhan Anda.
