import os
import datetime
import tabulate
import csv
from time import sleep
import pandas as pd


def fungsi_awal():
    print('='*100)
    print("||                     //                SELAMAT DATANG                    \\\\                     ||")
    print("||                    |||           Program Manajemen Laundry              |||                      ||")
    print("||                      \\\\                                              //                        ||")
    print('='*100)
    sleep(0.5)
    print("\nApakah anda sudah membuat akun?")
    while True:
        ipt = input("ya/tidak: ").lower()
        if ipt == 'ya':
            sign_in()
            break
        elif ipt == "tidak":
            sign_up()
            break
        else:
            print('\n>>> Masukkan jawaban yang benar! <<<\n')
            continue

#fungsi login dan register
def sign_in():
    os.system('cls' if os.name == 'nt' else 'clear')
    df = pd.read_csv('admin.csv')
    print('-------------------- SIGN IN --------------------\n')

    while True:
        username = input("Masukkan Username: ")
        password = int(input("Masukkan Password (angka): "))
        indeks = (df['Username'] == id).idxmax()
        if username in df['Username'].values and password in df['Password'].values:
            user_index = df.index[df['Username'] == username].tolist()[0]
            if df.loc[user_index, 'Password'] == password:
                menu()
                break
            else:
                print('\n>>> Password anda salah! <<<\n')
                continue
        else:
            print('\n>>> Username tidak ditemukan <<<\n')

def sign_up():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('-------------------- SIGN UP --------------------\n')
    nama = input("Masukkan Nama: ")
    while True:
        username = input("Masukkan Username yang ingin digunakan: ")
        try:
            df = pd.read_csv('admin.csv')
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Nama', 'Username', 'Password'])

        if username in df['Username'].values:
            print('\n*** Username telah digunakan, masukkan username yang lain! ***\n')
            continue
        password = int(input("Masukkan Password yang ingin digunakan (angka): "))
        
        new_entry = pd.DataFrame([[nama, username, password]], columns=['Nama', 'Username', 'Password'])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv('admin.csv', index=False)

        while True:
            verif = int(input("Masukkan kembali Password yang ingin digunakan (angka): "))
            if password == verif:
                print("\nData anda sedang diproses.....")
                sleep(2)
                print('-'*57)
                print('         Anda berhasil mendaftar! Silahkan login         ')
                print('-'*57)
                sleep(2.5)
                sign_in()
                break
            else:
                print("\n>>> Password anda salah, silahkan masukkan kembali password anda! <<<\n")
                continue

    
# fungsi menu
def menu ():
    os.system('cls')
    print("""
=========================================================================
|                     _   _   _____   __  _   _   _                     |
|     ______         | \_/ | | ____| |  \| | | | | |         ______     |
|     ******         |  _  | | __|_  |  _  | | |_| |         ******     |
|                    |_| |_| |_____| |_| |_|  \___/                     |
|                               M E N U                                 |
=========================================================================
silahkan pilih menu :
1. input data
2. edit data
3. cari data
4. Keluar 
          """)
    
    while True :
        pilihan = input("Pilih menu(1/2/3/4) : ")
        if pilihan == '1' :
            input_data()
            break
        elif pilihan == '2' :
            edit_data()
            break
        elif pilihan == '3' :
            cari_data()
            break
        elif pilihan == '4' :
            keluar()
            break
        else :
            print(f' >>> {pilihan} tidak ada di pilihan <<< ')
            continue


#                                               INPUT DATA

#fungsi input data
def input_data():
    os.system('cls' if os.name == 'nt' else 'clear')
    nama = input("Masukkan nama pelanggan: ")
    no_hp = int(input("Masukkan nomor handphone pelanggan: "))
    tanggal_masuk = datetime.date.today()

    data = pd.read_csv('jasa.csv')

    print(tabulate.tabulate(data, headers=["id", "jenis", "lama pengerjaan", "harga"], tablefmt="grid", showindex=False))

    # Determine the next nota ID
    if os.path.exists('nota.csv'):
        nota_data = pd.read_csv('nota.csv')
        if not nota_data.empty:
            nota_id = nota_data['id'].max() + 1
        else:
            nota_id = 1
    else:
        nota_id = 1

    semua_layanan = []
    totalakhir = 0

    while True:
        id_selected = input("Masukkan ID Layanan (1-9): ")
        if id_selected not in map(str, data['id'].tolist()):
            print(f'>>> {id_selected} tidak ada di pilihan. Silakan coba lagi. <<<')
            continue
        else:
            berat1 = float(input("Masukkan Berat / kg: "))
            selected_service = data[data['id'] == int(id_selected)]
            harga_per_kg = selected_service['harga'].values[0]
            lama_pengerjaan = int(selected_service['lama pengerjaan'].values[0])

            harga_per_hari = harga_per_kg / lama_pengerjaan
            if harga_per_hari > 15000:
                print(f">>> Harga per hari {harga_per_hari} lebih dari 15000, tidak bisa input layanan ini. <<<")
                continue
            
            total_harga = berat1 * harga_per_kg
            jenis_layanan = selected_service['jenis'].values[0]
            tanggal_diambil = tanggal_masuk + datetime.timedelta(days=lama_pengerjaan)

            data_to_append1 = pd.DataFrame({
                'id': [nota_id],
                'Nama Pelanggan': [nama],
                'Nomor HP': [no_hp],
                'Tanggal Masuk': [tanggal_masuk],
                'Tanggal Diambil': [tanggal_diambil],
                'Jenis Layanan': [jenis_layanan],
                'Berat (kg)': [berat1],
                'Harga per kg': [harga_per_kg],
                'Total Harga': [total_harga],
                'Status': ['belum selesai']
            })

            data_to_append1.to_csv('nota.csv', mode='a', header=not os.path.exists('nota.csv'), index=False)
            print(">>>>>> Data berhasil ditambahkan! <<<<<< \n")
            sleep(1)

            jasa2 = input("Apakah ingin menambahkan layanan lain? (ya/tidak): ").lower()

            semua_layanan.append({
                "jenis": jenis_layanan,
                "berat": berat1,
                "harga_per_kg": harga_per_kg,
                "total_harga": total_harga
            })

            totalakhir += total_harga

            while True:
                if jasa2 == 'ya':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(tabulate.tabulate(data, headers=["id", "jenis", "lama pengerjaan", "harga"], tablefmt="grid", showindex=False))
                    id_selected2 = input("Masukkan ID Layanan (1-9): ")
                    if id_selected2 not in map(str, data['id'].tolist()):
                        print(f'>>> {id_selected2} tidak ada di pilihan. Silakan coba lagi. <<<')
                        continue
                    selected_service2 = data[data['id'] == int(id_selected2)]
                    lama_pengerjaan2 = int(selected_service2['lama pengerjaan'].values[0])
                    if lama_pengerjaan2 != lama_pengerjaan:
                        print("Tanggal pengambilan berbeda, buat di nota lain!")
                        sleep(1.5)
                        continue
                    else:
                        berat = float(input("Masukkan Berat / kg: "))
                        harga_per_kg2 = selected_service2['harga'].values[0]
                        total_harga2 = berat * harga_per_kg2
                        jenis_layanan2 = selected_service2['jenis'].values[0]
                        tanggal_diambil2 = tanggal_masuk + datetime.timedelta(days=lama_pengerjaan2)

                        data_to_append2 = pd.DataFrame({
                            'id': [nota_id],
                            'Nama Pelanggan': [nama],
                            'Nomor HP': [no_hp],
                            'Tanggal Masuk': [tanggal_masuk],
                            'Tanggal Diambil': [tanggal_diambil2],
                            'Jenis Layanan': [jenis_layanan2],
                            'Berat (kg)': [berat],
                            'Harga per kg': [harga_per_kg2],
                            'Total Harga': [total_harga2],
                            'Status': ['belum selesai']
                        })

                        data_to_append2.to_csv('nota.csv', mode='a', header=False, index=False)
                        print(">>>>>> Data berhasil ditambahkan! <<<<<<\n")
                        sleep(1)

                        totalakhir += total_harga2

                    semua_layanan.append({
                        "jenis": jenis_layanan2,
                        "berat": berat,
                        "harga_per_kg": harga_per_kg2,
                        "total_harga": total_harga2
                    })
                    jasa3 = input("Apakah ingin menambahkan layanan lain? (ya/tidak): ").lower()

                    if jasa3 == 'ya':
                        continue
                    else:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("=============================== NOTA =============================")
                        print(f"ID Nota              : {nota_id}")
                        print(f"Nama                 : {nama}")
                        print(f"No HP                : {no_hp}")
                        print(f"tanggal pengambilan  : {tanggal_diambil}\n")
                        print(tabulate.tabulate(semua_layanan, headers='keys', tablefmt="grid"))
                        print(f"\nTOTAL                                                       {int(totalakhir)}")
                        print(f"BELUM DIAMBIL                                                    ")
                        print("==================================================================")
                        break

                elif jasa2 == 'tidak':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("=============================== NOTA =============================")
                    print(f"ID Nota              : {nota_id}")
                    print(f"Nama                 : {nama}")
                    print(f"No HP                : {no_hp}")
                    print(f"tanggal pengambilan  : {tanggal_diambil}\n")
                    print(tabulate.tabulate(semua_layanan, headers='keys', tablefmt="grid"))
                    print(f"\nTOTAL                                                       {int(totalakhir)}")
                    print(f"BELUM DIAMBIL                                                    ")
                    print("==================================================================")
                    break

            while True:
                tanya = input("\nApakah anda ingin kembali ke menu? (ya/tidak): ").lower()
                if tanya == 'ya':
                    menu()
                    break
                elif tanya == 'tidak':
                    break
                else:
                    print("Berikan jawaban yang benar!")
                    continue
        break



                   
#                                           CARI DATA
#fitur --> cari data, tampilkan data                                
def cari_data():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('-------------------- DATA --------------------\n')

        try:
            df = pd.read_csv('nota.csv')
        except FileNotFoundError:
            print("File nota.csv tidak ditemukan.")
            return

        print("Pilih opsi:")
        print("1. Cari data ")
        print("2. Tampilkan data ")
        print("3. Kembali")

        while True:
            choice = input("Masukkan pilihan (1/2/3): ").strip()
            if choice == '1':
                csv_file = "nota.csv"  
                phone_number = int(input("masukkan nomor hp : ")) 
                result = search_by_phone(csv_file, phone_number)
                print(result)
                break
        
            elif choice == '2':
                show_pending_orders(df)
                break
                    
            elif choice == '3':
                menu()
                break

            else:
                print("Pilihan tidak valid.")
                continue

        #while True:
        #    choice1 = input("Apakah Anda ingin kembali ke menu? (Ya/Tidak): ").strip().lower()
        #    if choice1 == 'ya':
        #        cari_data()
        #        break
        #    elif choice1 == 'tidak':
        #        keluar()
        #        break
        break
            
# ------------
def binary_search(arr, target, find_first):
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            if find_first:
                right = mid - 1
            else:
                left = mid + 1
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result

def search_by_phone(csv_file, phone_number):
    data = pd.read_csv(csv_file)
    sorted_indices = sorted(range(len(data['NomorHP'])), key=lambda k: data['NomorHP'][k])
    sorted_phone_numbers = sorted(data['NomorHP'].tolist())
    first_index = binary_search(sorted_phone_numbers, phone_number, True)
    if first_index == -1:
        return "Data tidak ditemukan."

    last_index = binary_search(sorted_phone_numbers, phone_number, False)
    result_indices = sorted_indices[first_index:last_index + 1]
    result = data.iloc[result_indices]
    return tabulate.tabulate(result, headers="keys", tablefmt="grid", showindex=False)

def show_pending_orders(df):
    os.system('cls' if os.name == 'nt' else 'clear')
    df_pending = df[df['status'] == 'belum selesai'].copy()
    df_pending['tanggal_diambil'] = pd.to_datetime(df_pending['tanggal_diambil'], format='%Y-%m-%d')
    if not df_pending.empty:
        merge_sort(df_pending, 'tanggal_diambil')
        print(tabulate.tabulate(df_pending, headers='keys', tablefmt='grid'))
    else:
        print("\nTidak ada pesanan yang belum selesai.")
    
    while True:
        choice = input("Apakah Anda ingin kembali (Ya/Tidak): ").strip().lower()
        if choice == 'ya':
            cari_data()
            break
        elif choice == 'tidak':
            keluar()
        else:
            print("Masukkan pilihan yang valid (Ya/Tidak)")
            continue

#                                                         EDIT DATA

#fitur --> ubah status, tambah data, edit data
def edit_data():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('-------------------- MENU --------------------\n')
    print('1. Ubah Status Pesanan')
    print('2. Edit Data Jasa')
    print('3. Tambah Data Jasa')
    print('4. Kembali')
    choice = input("Masukkan pilihan menu: ").strip()

    if choice == '1':
        # sub menu --> ubah status
        print('\n-------------------- UBAH STATUS PESANAN --------------------\n')
        csv_file = 'nota.csv'
        phone_number = int(input("Masukkan nomor hp: "))
        nama_kolom = 'status'
        
        # Check current status
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            current_status = None
            for row in reader:
                if int(row['NomorHP']) == phone_number:
                    current_status = row[nama_kolom]
                    break
        
        if current_status == 'selesai':
            nilai_baru = 'tidak jelas'
        else:
            nilai_baru = 'selesai'
        
        result = change_column_by_phone(csv_file, phone_number, nama_kolom, nilai_baru)
        print(result)
        
        while True:
            tanya = input("Apakah anda ingin kembali ke menu? (ya/tidak): ").strip().lower()
            if tanya == 'ya':
                edit_data()
                break
            elif tanya == 'tidak':
                break
            else:
                print("Jawaban tidak valid. Silakan coba lagi.")
                continue
    elif choice == '2':
        try:
            df_jasa = pd.read_csv('jasa.csv')
        except FileNotFoundError:
            print("File jasa.csv tidak ditemukan.")
            return
        print("Data Jasa yang Tersedia:")
        print(df_jasa)
        edit_data_jasa(df_jasa)
        while True:
            tanya = input("Apakah anda ingin kembali ke menu? (ya/tidak): ").strip().lower()
            if tanya == 'ya':
                edit_data() 
                break
            elif tanya == 'tidak':
                break
            else:
                print("Jawaban tidak valid. Silakan coba lagi.")
                continue


    elif choice == '3':
        try:
            df_jasa = pd.read_csv('jasa.csv')
        except FileNotFoundError:
            print("File jasa.csv tidak ditemukan.")
            return
        tambah_data_jasa(df_jasa)

    elif choice == '4' :
        menu()

    else:
        print("Pilihan tidak valid.")


def edit_data_jasa(df):
    print('\n----- EDIT DATA JASA -----\n')
    print(tabulate.tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    
    while True:
        id_jasa = input("Masukkan ID Jasa yang ingin diedit: ").strip()
        if id_jasa in df['id'].astype(str).values:
            kolom = input("Masukkan nama kolom yang ingin diubah (jenis/lama pengerjaan/harga): ").strip().lower()
            if kolom in df.columns:
                new_value = int(input(f"Masukkan nilai baru untuk kolom '{kolom}': "))
                df.loc[df['id'].astype(str) == id_jasa, kolom] = new_value
                df.to_csv('jasa.csv', index=False)
                print("Data jasa berhasil diubah.")
                
                while True:
                    tanya = input("Apakah anda ingin kembali ke menu? (ya/tidak): ").strip().lower()
                    if tanya == 'ya':
                        edit_data() 
                        break
                    elif tanya == 'tidak':
                        break
                    else:
                        print("Jawaban tidak valid. Silakan coba lagi.")
                        continue
            else:
                print("Kolom tidak valid.")
                continue
        else:
            print("ID Jasa tidak ditemukan.")
            continue


def change_column_by_phone(csv_file, phone_number, column_name, new_value):

    data = pd.read_csv(csv_file)

    indices = data[data['NomorHP'] == phone_number].index

    if not indices.empty:
        for index in indices:
            data.loc[index, column_name] = new_value
        
        data.to_csv(csv_file, index=False)
        return "Data berhasil diperbarui"
    else:
        return "nomor HP tidak ditemukan"
    

def merge_sort(df, col):
        if len(df) > 1:
            mid = len(df) // 2
            left_half = df.iloc[:mid].copy()
            right_half = df.iloc[mid:].copy()
            merge_sort(left_half, col)
            merge_sort(right_half, col)
            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                if left_half.iloc[i][col] < right_half.iloc[j][col]:
                    df.iloc[k] = left_half.iloc[i]
                    i += 1
                else:
                    df.iloc[k] = right_half.iloc[j]
                    j += 1
                k += 1
            while i < len(left_half):
                df.iloc[k] = left_half.iloc[i]
                i += 1
                k += 1
            while j < len(right_half):
                df.iloc[k] = right_half.iloc[j]
                j += 1
                k += 1        

#sub menu --> tambah data
def tambah_data_jasa(df):
    print('\n----- TAMBAH DATA JASA -----\n')
    jenis = input("Masukkan Jenis Jasa: ").strip()
    lama_pengerjaan = input("Masukkan Lama Pengerjaan (hari): ").strip()
    harga = input("Masukkan Harga (per kg): ").strip()
    try:
        last_id = int(df['id'].iloc[-1]) 
        new_id = last_id + 1 
    except IndexError:
        new_id = 1  
    with open('jasa.csv', 'a') as f:
        f.write(f"{new_id},{jenis},{lama_pengerjaan},{harga}\n")
    print("Data jasa berhasil ditambahkan.")
    while True:
            choice = input("Apakah Anda ingin kembali (Ya/Tidak): ").strip().lower()
            if choice == 'ya':
                edit_data()
                break
            elif choice == 'tidak':
                menu()
                break
            else:
                print("Masukkan pilihan yang valid (Ya/Tidak)")
                continue


#fungsi keluar --> fitur untuk keluar
def keluar() :
    tanya = input('Apakah anda yakin ingin keluar dari program? (ya/tidak) : ').lower()
    while True :
        if tanya == 'ya' :
            break
        elif tanya == 'tidak' :
            menu()
            break
    

fungsi_awal()
