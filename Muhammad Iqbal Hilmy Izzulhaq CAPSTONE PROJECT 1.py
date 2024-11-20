from datetime import datetime, timedelta
from tabulate import tabulate
import re

# Membuat data dummy untuk jadwal
jadwal = [
    {
        'nama': 'Andi Pratama',
        'lapangan': 1,
        'waktu_mulai': datetime(2024, 11, 28, 19, 0),
        'durasi': 2,
        'waktu_akhir': datetime(2024, 11, 28, 21, 0),
        'total_harga': 130000,  # 2 jam * 65000
        'status_pembayaran': 'Lunas'
    },
    {
        'nama': 'Budi Santoso',
        'lapangan': 2,
        'waktu_mulai': datetime(2024, 11, 29, 19, 0),
        'durasi': 3,
        'waktu_akhir': datetime(2024, 11, 29, 22, 0),
        'total_harga': 195000,  # 3 jam * 65000
        'status_pembayaran': 'DP 50%'
    },
    {
        'nama': 'Citra Dewi',
        'lapangan': 3,
        'waktu_mulai': datetime(2024, 11, 23, 20, 0),
        'durasi': 2,
        'waktu_akhir': datetime(2024, 11, 23, 22, 0),
        'total_harga': 160000,  # 2 jam * 80000 (Weekend)
        'status_pembayaran': 'Pending'
    },
    {
        'nama': 'Dewi Lestari',
        'lapangan': 4,
        'waktu_mulai': datetime(2024, 11, 23, 19, 0),
        'durasi': 1,
        'waktu_akhir': datetime(2024, 11, 23, 20, 0),
        'total_harga': 65000,  # 1 jam * 65000
        'status_pembayaran': 'Lunas'
    },
    {
        'nama': 'Eka Putri',
        'lapangan': 5,
        'waktu_mulai': datetime(2024, 11, 18, 19, 0),
        'durasi': 1,
        'waktu_akhir': datetime(2024, 11, 18, 21, 0),
        'total_harga': 65000,  # 2.5 jam * 65000
        'status_pembayaran': 'Pending'
    }
]

feedback = []  # Menyimpan feedback dan permintaan penghapusan jadwal

# Fungsi untuk menghitung harga booking Weekday dan Weekend
def hitung_harga(tanggal_penyewaan, durasi):
    # Harga weekend 80000/jam, Weekday 65000/jam
    harga_per_jam = 80000 if tanggal_penyewaan.weekday() >= 5 else 65000 
    return harga_per_jam * durasi

# Fungsi untuk mengecek apakah ada bentrokan jadwal pemesanan
def cek_bentrok(lapangan, jam_mulai, durasi):
    waktu_akhir_input = jam_mulai + timedelta(hours=durasi)  # Hitung waktu akhir input
    for j in jadwal:
        if j['lapangan'] == lapangan:  # Cek apakah lapangan sama
            jadwal_akhir = j['waktu_mulai'] + timedelta(hours=j['durasi'])  # Hitung waktu akhir jadwal
            # Kondisi bentrok: waktu mulai atau waktu akhir tumpang tindih
            if (jam_mulai < jadwal_akhir) and (waktu_akhir_input > j['waktu_mulai']):
                print(f"Bentrok dengan jadwal lain: Nama = {j['nama']}, Lapangan {lapangan}, pada pukul {j['waktu_mulai']} - {jadwal_akhir}")
                print(lihat_daftar_pemesanan())
                return True
    return False


        
# Fungsi untuk menentukan jadwal operasional
def cek_jam_operasional(tanggal_penyewaan, jam_mulai, durasi):
    # Membedakan jam tutup Weekend = 24:00 dan Weekday = 23:00
    jam_tutup = 24 if tanggal_penyewaan.weekday() >= 5 else 23
    if jam_mulai.hour < 19 or jam_mulai.hour >= jam_tutup: # Agar konsumen tidak dapat memesan di luar jam operasional
        print(f"Jam mulai harus antara 19:00 dan {jam_tutup}:00.")
        return False
    # Membuat condition untuk memastikan durasi pemesanan tidak melebihi jam tutup
    if jam_mulai.hour + durasi > jam_tutup:
        print(f"Durasi penyewaan melebihi jam tutup ({jam_tutup}:00). Silakan pilih durasi yang lebih pendek.")
        return False
    if durasi < 1:
        print("Durasi minimal 1 jam.")
        return False
    return True

# Fungsi untuk menginput tanggal pemesanan
def input_datetime(prompt, date_format='%d-%m-%Y'): # membuat format input tanggal menjadi dd-mm-yyyy
    while True:        
        try:
            tanggal = input(prompt)
            # Parsing tanggal dengan format dd-mm-yyyy
            tanggal_input = datetime.strptime(tanggal, date_format)
            
            # Cek apakah tanggal input sudah lewat
            if tanggal_input < datetime.now():
                print("Tidak dapat memesan, hari sudah lewat.")
                continue
            
            # Cek apakah pemesanan dilakukan minimal 2 hari sebelum menggunakan lapangan
            if tanggal_input < datetime.now() + timedelta(days=2):
                print("Hanya dapat memesan. Pemesanan hanya dapat dilakukan minimal 2 hari sebelumnya.")
                continue
            
            return tanggal_input
        except ValueError:
            print(f"Format tanggal tidak valid. Gunakan format {date_format}.")

# Fungsi untuk menu autentikasi pengelola lapangan
def autentikasi_pengelola():
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    return username == 'iqbal' and password == 'iqbal'
# Fungsi untuk Penyewa Lapangan
def tambah_penyewaan():
    while True:
        nama = input("Masukkan nama penyewa: ")
        if re.fullmatch(r"[A-Za-z\s]+", nama):
            break  # Keluar dari loop jika nama valid
        else:
            print("Nama hanya boleh berisi huruf dan spasi.")
    # Input tanggal penyewaan dengan validasi
    tanggal_str = input_datetime("Masukkan tanggal penyewaan (dd-mm-yyyy): ")
    # Loop untuk memastikan input jam berada dalam jam operasional

    while True:
        jam_mulai_str = input("Masukkan jam mulai penyewaan (HH:MM): ")
        try:
            jam_mulai = datetime.strptime(f"{tanggal_str.strftime('%d-%m-%Y')} {jam_mulai_str}", '%d-%m-%Y %H:%M')
            # Cek apakah jam mulai dan durasi valid sesuai jam operasional
            durasi = float(input("Masukkan durasi penyewaan dalam jam: "))
            lapangan = int(input("Pilih lapangan (1-5): "))
            if cek_jam_operasional(tanggal_str, jam_mulai, durasi):
                if not cek_bentrok(lapangan, jam_mulai, durasi):
                    break  # Keluar dari loop jika valid
        except ValueError:
            print("Format jam tidak valid. Harap masukkan dalam format HH:MM.")
    
    # Pilih lapangan
    while True:
        try:
            if lapangan < 1 or lapangan > 5:
                print("Lapangan harus dipilih antara 1 dan 5.")
            else:
                break
        except ValueError:
            print("Input lapangan tidak valid. Harap masukkan angka antara 1 dan 5.")

    
    # Menggabungkan tanggal dan jam untuk menghasilkan waktu mulai
    jam_mulai = datetime.strptime(f"{tanggal_str.strftime('%d:%m:%Y')} {jam_mulai_str}", '%d:%m:%Y %H:%M')
    
    # Cek apakah waktu operasional valid dan tidak bentrok
    if cek_jam_operasional(jam_mulai.date(), jam_mulai, durasi) and not cek_bentrok(lapangan, jam_mulai, durasi):
        jadwal.append({
            'nama': nama,
            'lapangan': lapangan,
            'waktu_mulai': jam_mulai,
            'durasi': durasi,
            'waktu_akhir': jam_mulai + timedelta(hours=durasi),
            'total_harga': hitung_harga(jam_mulai.date(), durasi),
            'status_pembayaran': 'Pending'
        })
        print(f"Pemesanan untuk {nama} berhasil ditambahkan.")
        return lihat_daftar_pemesanan()

# Fungsi untuk feedback customer
def feedback_customer():
    print("\n==== Menu Feedback Customer ====")
    while True:
        nama = input("Masukkan nama penyewa: ")
        pemesanan_ditemukan = False
        for j in jadwal:
            if j['nama'].lower() == nama.lower():
                pemesanan_ditemukan = True
                print("1. Ajukan Penghapusan Jadwal")
                print("2. Ajukan Perubahan Jadwal")
                print("3. Kirim Feedback")
                print("4. Kembali")
                pilihan = input("Pilih menu (1-5): ")
                if pilihan == '1':
                    feedback.append({
                        'nama': nama,
                        'tipe': 'hapus',
                        'detail': f"Mohon jadwal pada {j['waktu_mulai'].strftime('%d-%m-%Y %H:%M')} di lapangan {j['lapangan']} dihapus."
                    })
                    print("Permintaan penghapusan telah diajukan.")
                    return
                elif pilihan == '2':  # Ajukan Perubahan Jadwal
                        while True:
                            try:
                                # Input tanggal baru
                                tanggal_str = input("Masukkan tanggal baru (dd-mm-yyyy): ")
                                tanggal_baru = datetime.strptime(tanggal_str, "%d-%m-%Y")
                                waktu_sekarang = datetime.now()
                                
                                # Validasi H-2
                                if tanggal_baru < waktu_sekarang + timedelta(days=2):
                                    print("Tanggal baru tidak valid atau telah lewat. Perubahan jadwal hanya dapat dilakukan minimal H-2.")
                                    continue
                                while True:
                                    try:
                                        # Input jam mulai penyewaan baru
                                        jam_mulai_str = input("Masukkan jam mulai penyewaan (HH:MM): ")
                                        jam_mulai_baru = datetime.strptime(
                                            f"{tanggal_baru.strftime('%d-%m-%Y')} {jam_mulai_str}", '%d-%m-%Y %H:%M'
                                        )
                                        
                                        # Ambil data durasi dan lapangan dari pemesanan sebelumnya
                                        durasi = j['durasi']
                                        lapangan = j['lapangan']

                                        # Validasi jam operasional
                                        if not cek_jam_operasional(tanggal_baru, jam_mulai_baru, durasi):
                                            print("Jam mulai atau durasi di luar jam operasional.")
                                            continue

                                        # Validasi bentrok jadwal
                                        if cek_bentrok(lapangan, jam_mulai_baru, durasi):
                                            print("Jadwal baru bentrok dengan jadwal lain.")
                                            continue

                                        # Jika valid, ajukan permintaan perubahan
                                        feedback.append({
                                            'nama': nama,
                                            'tipe': 'ubah',
                                            'detail': f"Ubah jadwal dari {j['waktu_mulai'].strftime('%d-%m-%Y %H:%M')} "
                                                    f"ke {jam_mulai_baru.strftime('%d-%m-%Y %H:%M')} di lapangan {lapangan}.",
                                            'waktu_baru': jam_mulai_baru,
                                            'durasi': durasi,
                                            'lapangan': lapangan
                                        })
                                        print("Permintaan perubahan jadwal telah diajukan.")
                                        return
                                    
                                    except ValueError:
                                        print("Format jam tidak valid. Harap masukkan dalam format HH:MM.")
                            except ValueError:
                                print("Format tanggal tidak valid. Harap masukkan dalam format dd-mm-yyyy.")                    
                elif pilihan == '3':
                    masukan = input("Masukkan feedback Anda: ")
                    feedback.append({
                        'nama': nama,
                        'tipe': 'feedback',
                        'detail': masukan
                    })
                    print("Feedback Anda telah dikirim.")
                    return
                elif pilihan =='4':
                    return
                else:
                    print("Pilihan tidak valid.")
                return
        if not pemesanan_ditemukan:
            print("Nama tidak ditemukan dalam daftar jadwal. Silakan lakukan pemesanan terlebih dahulu.")
            while True:
                pilihan = input("Pilih opsi: 1. Coba lagi  2. Kembali: ")
                if pilihan == '1':
                    break 
                elif pilihan == '2':
                    return  
                else:
                    print("pilihan tidak valid, masukan pilihan 1 atau 2")
            
# Fungsi untuk menu pengelola (persetujuan permintaan)
def menu_feedback_pengelola():
    print("\n==== Menu Permintaan Penyewa ====")
    if not feedback:
        print("Belum ada permintaan.")
        return

    for i, f in enumerate(feedback, start=1):
        print(f"{i}. [{f['tipe'].upper()}] {f['nama']}: {f['detail']}")
    pilihan = input("Pilih nomor permintaan untuk ditindaklanjuti (atau '0' untuk kembali): ")

    if pilihan.isdigit() and 0 <= int(pilihan) <= len(feedback):
        pilihan = int(pilihan)
        if pilihan == 0:
            return
        
        permintaan = feedback.pop(pilihan - 1)
        
        if permintaan['tipe'] == 'hapus':  # Permintaan penghapusan jadwal
            for i, j in enumerate(jadwal):
                if j['nama'].lower() == permintaan['nama'].lower():
                    del jadwal[i]
                    print(f"Jadwal milik {permintaan['nama']} telah dihapus.")
                    break

        elif permintaan['tipe'] == 'ubah':  # Permintaan perubahan jadwal
            print(f"\nPermintaan perubahan jadwal oleh {permintaan['nama']}:")
            print(f"Dari: {permintaan['detail'].split(' ke ')[0]}")
            print(f"Ke: {permintaan['detail'].split(' ke ')[1]}")
            konfirmasi = input("Apakah Anda menyetujui perubahan ini? (y/n): ").lower()
            if konfirmasi == 'y':
                for j in jadwal:
                    if j['nama'].lower() == permintaan['nama'].lower():
                        j['waktu_mulai'] = permintaan['waktu_baru']
                        j['lapangan'] = permintaan['lapangan']
                        print(f"Jadwal milik {permintaan['nama']} telah diperbarui.")
                        break
            else:
                print("Permintaan perubahan jadwal ditolak.")

    else:
        print("Pilihan tidak valid.")
        while True:
            pilihan = input("Pilih opsi: 1. Coba lagi  2. Kembali: ")
            if pilihan == '1':
                break
            if pilihan == '2':
                return
            print("Pilihan tidak valid. Masukkan pilihan 1 atau 2.")


# Fungsi untuk menampilkan jadwal pemesanan
def lihat_daftar_pemesanan():
    if jadwal:
        headers = ['Nama Penyewa', 'Lapangan', 'Tanggal', 'Waktu Mulai', 'Waktu Akhir', 'Durasi (Jam)', 'Total Harga', 'Status Pembayaran']
        data = []
        for j in jadwal:
            data.append([j['nama'], j['lapangan'], j['waktu_mulai'].strftime('%d-%m-%Y'), j['waktu_mulai'].strftime('%H:%M'), j['waktu_akhir'].strftime('%H:%M'), j['durasi'], j['total_harga'], j['status_pembayaran']])
        print(tabulate(data, headers, tablefmt="fancy_grid"))
    else:
        print("Belum ada pemesanan.")

# Fungsi untuk menu utama pengelola lapangan
def menu_pengelola():
        while True:
            print("\n==== Menu Pengelola ====")
            print("1. Lihat Daftar Pemesanan")
            print("2. Lihat Status Pembayaran")
            print("3. Tinjau Permintaan Penyewa")
            print("4. Kembali")
            
            sub_pilihan = input("Pilih menu (1-4): ")
            if sub_pilihan == '1':
                lihat_daftar_pemesanan()
            elif sub_pilihan == '2':
                lihat_daftar_pemesanan()  # Bisa diubah jika ingin menambahkan detil pembayaran
            elif sub_pilihan == '3':
                menu_feedback_pengelola()
            elif sub_pilihan == '4':
                return main()
            else:
                print("Pilihan tidak valid.")
                
def lihat_pesanan_saya(nama_penyewa):
    print("\n==== Pesanan Saya ====")
    found = False
    for j in jadwal:
        if j['nama'].lower() == nama_penyewa.lower():
            print(f"Nama: {j['nama']}")
            print(f"Total: {j['total_harga']}")
            print(f"Status Pembayaran: {j['status_pembayaran']}")
            print("\n1. Bayar DP 50%")
            print("2. Bayar Penuh")
            print("0. Kembali")
            while True:
                pilihan = input("Pilih pembayaran (1-2, atau 0 untuk kembali): ")
                
                # Opsi DP 50%
                if pilihan == '1' and j['status_pembayaran'] == 'Pending':
                    dp = j['total_harga'] / 2
                    konfirmasi = input(f"Apakah Anda yakin ingin membayar DP sebesar {dp}? (y/n): ").lower()
                    if konfirmasi == 'y':
                        j['status_pembayaran'] = 'DP 50%'
                        print("Pembayaran DP 50% telah diterima. Status pembayaran diperbarui.")
                        return lihat_daftar_pemesanan()
                    elif konfirmasi == 'n':
                        print("Pembayaran dibatalkan.")
                        return
                    
                # Opsi Bayar Penuh
                elif pilihan == '2' and j['status_pembayaran'] == 'Pending':
                    total = j['total_harga']
                    konfirmasi = input(f"Apakah Anda yakin ingin membayar penuh sebesar {total}? (y/n): ").lower()
                    if konfirmasi == 'y':
                        j['status_pembayaran'] = 'Lunas'
                        print("Pembayaran penuh diterima. Status pembayaran diperbarui.")
                        return lihat_daftar_pemesanan()
                    elif konfirmasi == 'n':
                        print("Pembayaran dibatalkan.")
                        return
                    
                # Kembali ke menu sebelumnya
                elif pilihan == '0':
                    print("Kembali ke menu sebelumnya.")
                    return
                
                # Input tidak valid
                else:
                    print("Input tidak valid atau pembayaran sudah diproses. Silakan coba lagi.")
    if not found:  # Jika tidak ditemukan nama penyewa
        print(f"Mohon maaf, nama {nama_penyewa} tidak terdaftar dalam daftar pemesanan, silahkan coba lagi.")
        

# Fungsi untuk menu utama penyewa
def menu_penyewa():
    while True:
        print("\n==== Menu Penyewa ====")
        print("1. Lihat Daftar Pemesanan")
        print("2. Tambah Pemesanan")
        print("3. Lihat Pesanan Saya")
        print("4. Feedback / Permintaan Perubahan")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ")
        if pilihan == '1':
            lihat_daftar_pemesanan()
        elif pilihan == '2':
            tambah_penyewaan()
        elif pilihan == '3':
            nama_penyewa = input("Masukkan nama Anda: ")
            lihat_pesanan_saya(nama_penyewa)
        elif pilihan == '4':
            feedback_customer()
        elif pilihan == '5':
            return main()
        else:
            print("Pilihan tidak valid.")

# Program utama
def main():
    print("Selamat datang di Sistem Pemesanan Lapangan Badminton!")
    print("1. Pengelola Lapangan")
    print("2. Penyewa Lapangan")
    print("3. Exit Program")
    jenis_user = int(input("Masukan pilihan menu (1-3): "))

    if jenis_user == 1:
        while True:
            if autentikasi_pengelola():
                menu_pengelola()
            else:
                print("Username atau Password Anda salah.")
                while True:
                    pilihan = input("Pilih opsi: 1. Coba lagi  2. Kembali: ")
                    if pilihan == '1':
                        continue
                    elif pilihan == '2':
                        return main()
                    else:
                        print("pilihan tidak valid, masukan pilihan 1 atau 2")
    elif jenis_user == 2:
        menu_penyewa()
    elif jenis_user == 3:
        print("Terima Kasih telah menggunakan program Sistem Pemesanan Lapangan Badminton!")
        exit
    else:
        print("Pilihan tidak valid.")
        return

for i, j in enumerate(jadwal):
    if j['waktu_mulai'] < datetime.now():
        del jadwal[i]
        break

# Jalankan program utama
main()

print(feedback)