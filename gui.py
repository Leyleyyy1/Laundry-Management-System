import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from tabulate import tabulate
from datetime import datetime , timedelta
import pandas as pd

# Placeholder for admin data
admin_file = 'admin.csv'
jasa_file = 'jasa.csv'
nota_file = 'nota.csv'


# Sign In function
def sign_in():
    sign_in_frame = tk.Frame(root)
    sign_in_frame.pack(expand=True)


    def verify_sign_in():
        username = entry_username.get()
        password = entry_password.get()

        if not os.path.exists(admin_file):
            messagebox.showerror("Sign In", f"File {admin_file} tidak ditemukan!")
            return

        try:
            df = pd.read_csv(admin_file)
            print("Data dari admin.csv:")
            print(df)
            if (df['Username'] == username).any() and (df['Password'].astype(str) == password).any():
                messagebox.showinfo("Sign In", "Login berhasil!")
                sign_in_frame.destroy()
                show_menu()
            else:
                messagebox.showerror("Sign In", "Username atau Password salah!")
        except Exception as e:
            messagebox.showerror("Sign In", f"Terjadi kesalahan saat membaca file: {e}")

    tk.Label(sign_in_frame, text="Username:", font=("Arial", 16)).pack(pady=5)
    entry_username = tk.Entry(sign_in_frame, font=("Arial", 16))
    entry_username.pack(pady=5)
    tk.Label(sign_in_frame, text="Password:", font=("Arial", 16)).pack(pady=5)
    entry_password = tk.Entry(sign_in_frame, font=("Arial", 16), show='*')
    entry_password.pack(pady=5)
    tk.Button(sign_in_frame, text="Login", command=verify_sign_in, font=("Arial", 16)).pack(pady=5)
    tk.Button(sign_in_frame, text="Kembali", command=lambda: [sign_in_frame.destroy(), welcome_page()], font=("Arial", 16)).pack(pady=5)

# Sign Up function
def sign_up():
    sign_up_frame = tk.Frame(root)
    sign_up_frame.pack(expand=True)

    def register_user():
        nama = entry_nama.get()
        username = entry_username.get()
        password = entry_password.get()

        try:
            if os.path.exists(admin_file):
                df = pd.read_csv(admin_file)
            else:
                df = pd.DataFrame(columns=['Nama', 'Username', 'Password'])

            if username in df['Username'].values:
                messagebox.showerror("Sign Up", "Username telah digunakan!")
            else:
                new_entry = pd.DataFrame([[nama, username, password]], columns=['Nama', 'Username', 'Password'])
                df = pd.concat([df, new_entry], ignore_index=True)
                df.to_csv(admin_file, index=False)
                messagebox.showinfo("Sign Up", "Pendaftaran berhasil!")
                sign_up_frame.destroy()
                sign_in()
        except Exception as e:
            messagebox.showerror("Sign Up", f"Terjadi kesalahan saat menyimpan data: {e}")

    tk.Label(sign_up_frame, text="Nama:", font=("Arial", 16)).pack(pady=5)
    entry_nama = tk.Entry(sign_up_frame, font=("Arial", 16))
    entry_nama.pack(pady=5)
    tk.Label(sign_up_frame, text="Username:", font=("Arial", 16)).pack(pady=5)
    entry_username = tk.Entry(sign_up_frame, font=("Arial", 16))
    entry_username.pack(pady=5)
    tk.Label(sign_up_frame, text="Password:", font=("Arial", 16)).pack(pady=5)
    entry_password = tk.Entry(sign_up_frame, font=("Arial", 16), show='*')
    entry_password.pack(pady=5)
    tk.Button(sign_up_frame, text="Daftar", command=register_user, font=("Arial", 16)).pack(pady=5)
    tk.Button(sign_up_frame, text="Kembali", command=lambda: [sign_up_frame.destroy(), welcome_page()], font=("Arial", 16)).pack(pady=5)

# Input Data function
def input_data():
    input_data_frame = tk.Frame(root)
    input_data_frame.pack(expand=True)

    tk.Label(input_data_frame, text="Nama Pelanggan:", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=5, sticky='w')
    entry_nama_pelanggan = tk.Entry(input_data_frame, font=("Arial", 16))
    entry_nama_pelanggan.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(input_data_frame, text="Nomor HP Pelanggan:", font=("Arial", 16)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
    entry_no_hp = tk.Entry(input_data_frame, font=("Arial", 16))
    entry_no_hp.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(input_data_frame, text="Layanan yang Tersedia:", font=("Arial", 16)).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='w')

    # Create a Treeview to display the table
    columns = ('id', 'jenis', 'lama pengerjaan', 'harga')
    tree = ttk.Treeview(input_data_frame, columns=columns, show='headings')
    tree.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')

    # Define headings
    tree.heading('id', text='ID')
    tree.heading('jenis', text='Jenis')
    tree.heading('lama pengerjaan', text='Lama Pengerjaan')
    tree.heading('harga', text='Harga')

    # Define column widths
    tree.column('id', width=50, anchor='center')
    tree.column('jenis', width=200, anchor='center')
    tree.column('lama pengerjaan', width=150, anchor='center')
    tree.column('harga', width=100, anchor='center')

    # Add data to the treeview
    try:
        df_jasa = pd.read_csv(jasa_file)
        for index, row in df_jasa.iterrows():
            tree.insert('', tk.END, values=(row['id'], row['jenis'], row['lama pengerjaan'], row['harga']))
    except FileNotFoundError:
        messagebox.showerror("Error", "Data layanan tidak ditemukan!")

    tk.Label(input_data_frame, text="ID Layanan yang Dipilih:", font=("Arial", 16)).grid(row=4, column=0, padx=10, pady=5, sticky='w')
    entry_layanan = tk.Entry(input_data_frame, font=("Arial", 16))
    entry_layanan.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(input_data_frame, text="Berat Pakaian (kg):", font=("Arial", 16)).grid(row=5, column=0, padx=10, pady=5, sticky='w')
    entry_berat = tk.Entry(input_data_frame, font=("Arial", 16))
    entry_berat.grid(row=5, column=1, padx=10, pady=5)

    layanan_terpilih = []

    def tambah_layanan():
        layanan_id = entry_layanan.get()
        berat = entry_berat.get()
        try:
            df_jasa = pd.read_csv(jasa_file)
            layanan = df_jasa[df_jasa['id'] == int(layanan_id)].iloc[0]
            layanan_jenis = layanan['jenis']
            lama_pengerjaan = layanan['lama pengerjaan']
            harga = layanan['harga']

            if not layanan_terpilih or all(l['lama pengerjaan'] == lama_pengerjaan for l in layanan_terpilih):
                layanan_terpilih.append({
                    'id': layanan_id,
                    'jenis': layanan_jenis,
                    'lama pengerjaan': lama_pengerjaan,
                    'harga': harga,
                    'berat': berat
                })
                messagebox.showinfo("Layanan", f"Layanan {layanan_jenis} berhasil ditambahkan!")
            else:
                messagebox.showerror("Error", "Layanan dengan lama pengerjaan yang berbeda tidak bisa dipilih bersama!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def submit_data():
        nama = entry_nama_pelanggan.get()
        no_hp = entry_no_hp.get()

        try:
            tanggal_masuk = datetime.now().strftime('%Y-%m-%d')
            lama_pengerjaan = int(layanan_terpilih[0]['lama pengerjaan'])
            tanggal_diambil = (datetime.now() + timedelta(days=lama_pengerjaan)).strftime('%Y-%m-%d')

            if os.path.exists(nota_file):
                df_nota = pd.read_csv(nota_file)
            else:
                df_nota = pd.DataFrame(columns=['id', 'nama_pelanggan', 'NomorHP', 'tanggal_masuk', 'tanggal_diambil', 'jenis', 'berat(kg)', 'harga(kg)', 'total', 'status'])

            new_id = df_nota['id'].max() + 1 if not df_nota.empty else 1

            total = 0
            for layanan in layanan_terpilih:
                total += int(layanan['berat']) * int(layanan['harga'])
                new_entry = pd.DataFrame([[new_id, nama, no_hp, tanggal_masuk, tanggal_diambil, layanan['jenis'], layanan['berat'], layanan['harga'], total, 'belum selesai']], 
                                         columns=['id', 'nama_pelanggan', 'NomorHP', 'tanggal_masuk', 'tanggal_diambil', 'jenis', 'berat(kg)', 'harga(kg)', 'total', 'status'])
                df_nota = pd.concat([df_nota, new_entry], ignore_index=True)
            df_nota.to_csv(nota_file, index=False)

            nota_str = f"================ NOTA ================\n"
            nota_str += f"ID Nota      : {new_id}\n"
            nota_str += f"Nama         : {nama}\n"
            nota_str += f"No HP        : {no_hp}\n"
            nota_str += f"Tanggal Diambil : {tanggal_diambil}\n"
            nota_str += f"{'='*35}\n"
            nota_str += f"| {'Jenis':<20} | {'Berat':<5} | {'Harga/Kg':<10} | {'Total Harga':<10} |\n"
            nota_str += f"{'-'*35}\n"
            for layanan in layanan_terpilih:
                nota_str += f"| {layanan['jenis']:<20} | {layanan['berat']:<5} | {layanan['harga']:<10} | {int(layanan['berat']) * int(layanan['harga']):<10} |\n"
            nota_str += f"{'-'*35}\n"
            nota_str += f"TOTAL        : {total}\n"
            nota_str += f"BELUM DIAMBIL\n"
            nota_str += f"{'='*35}\n"
            messagebox.showinfo("Nota", nota_str)

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan data: {e}")

    tk.Button(input_data_frame, text="Tambah Layanan", command=tambah_layanan, font=("Arial", 16)).grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    tk.Button(input_data_frame, text="Submit", command=submit_data, font=("Arial", 16)).grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    tk.Button(input_data_frame, text="Kembali", command=lambda: [input_data_frame.destroy(), show_menu()], font=("Arial", 16)).grid(row=8, column=0, columnspan=2, padx=10, pady=10)

def lihat_nota():
    lihat_nota_frame = tk.Frame(root)
    lihat_nota_frame.pack(expand=True)

    tk.Label(lihat_nota_frame, text="Masukkan ID Nota:", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=5, sticky='w')
    entry_id_nota = tk.Entry(lihat_nota_frame, font=("Arial", 16))
    entry_id_nota.grid(row=0, column=1, padx=10, pady=5)

    def show_nota():
        id_nota = entry_id_nota.get()
        try:
            df_nota = pd.read_csv(nota_file)
            nota = df_nota[df_nota['id'] == int(id_nota)]
            if not nota.empty:
                nota_data = nota.to_dict('records')[0]
                jenis_layanan = nota['jenis'].tolist()
                berat = nota['berat(kg)'].tolist()
                harga = nota['harga(kg)'].tolist()
                total_harga = nota['total'].tolist()
                
                nota_str = f"================ NOTA ===============\n"
                nota_str += f"ID Nota      : {nota_data['id']}\n"
                nota_str += f"Nama         : {nota_data['nama_pelanggan']}\n"
                nota_str += f"No HP        : {nota_data['NomorHP']}\n"
                nota_str += f"Tanggal Masuk: {nota_data['tanggal_masuk']}\n"
                nota_str += f"Tanggal Diambil: {nota_data['tanggal_diambil']}\n"
                nota_str += f"{'='*35}\n"
                nota_str += f"| {'Jenis':<20} | {'Berat':<5} | {'Harga/Kg':<10} | {'Total Harga':<10} |\n"
                nota_str += f"{'-'*35}\n"
                for j, b, h, t in zip(jenis_layanan, berat, harga, total_harga):
                    nota_str += f"| {j:<20} | {b:<5} | {h:<10} | {t:<10} |\n"
                nota_str += f"{'-'*35}\n"
                nota_str += f"TOTAL        : {nota_data['total']}\n"
                nota_str += f"{nota_data['status'].upper()}\n"
                nota_str += f"{'='*35}\n"
                messagebox.showinfo("Nota", nota_str)
            else:
                messagebox.showinfo("Nota", "Nota tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat membaca data: {e}")

    tk.Button(lihat_nota_frame, text="Lihat Nota", command=show_nota, font=("Arial", 16)).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    tk.Button(lihat_nota_frame, text="Kembali", command=lambda: [lihat_nota_frame.destroy(), show_menu()], font=("Arial", 16)).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

def show_menu():
    menu_frame = tk.Frame(root)
    menu_frame.pack(expand=True)

    tk.Label(menu_frame, text="Menu", font=("Arial", 24)).pack(pady=10)

    tk.Button(menu_frame, text="Input Data", command=lambda: [menu_frame.destroy(), input_data()], font=("Arial", 16)).pack(pady=5)
    tk.Button(menu_frame, text="Lihat Nota", command=lambda: [menu_frame.destroy(), lihat_nota()], font=("Arial", 16)).pack(pady=5)
    tk.Button(menu_frame, text="Kembali", command=lambda: [menu_frame.destroy(), welcome_page()], font=("Arial", 16)).pack(pady=5)

def edit_data():
    # Clear the root frame before adding new widgets
    for widget in root.winfo_children():
        widget.destroy()
    
    edit_data_frame = tk.Frame(root)
    edit_data_frame.pack(expand=True)

    def ubah_status_pesanan():
        edit_data_frame.destroy()
        ubah_status_frame = tk.Frame(root)
        ubah_status_frame.pack(expand=True)

        # Frame untuk input nomor HP dan tombol cari
        input_frame = tk.Frame(ubah_status_frame)
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="Masukkan Nomor HP:", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=5)
        entry_no_hp = tk.Entry(input_frame, font=("Arial", 16))
        entry_no_hp.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(input_frame, text="Cari", command=lambda: cari_pesanan(entry_no_hp.get()), font=("Arial", 16)).grid(row=0, column=2, padx=10, pady=5)

        # Create a Treeview with a scrollbar
        tree_frame = tk.Frame(ubah_status_frame)
        tree_frame.pack(padx=10, pady=5, fill='both', expand=True)
        columns = ['id', 'nama_pelanggan', 'NomorHP', 'tanggal_masuk', 'tanggal_diambil', 'jenis', 'berat(kg)', 'harga(kg)', 'total', 'status']
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="extended")
        
        # Add a vertical scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)
        
        # Add columns and headers to the treeview with adjusted widths
        tree.heading('id', text='ID')
        tree.column('id', width=50, anchor='center')
        tree.heading('nama_pelanggan', text='Nama Pelanggan')
        tree.column('nama_pelanggan', width=150, anchor='center')
        tree.heading('NomorHP', text='Nomor HP')
        tree.column('NomorHP', width=100, anchor='center')
        tree.heading('tanggal_masuk', text='Tanggal Masuk')
        tree.column('tanggal_masuk', width=100, anchor='center')
        tree.heading('tanggal_diambil', text='Tanggal Diambil')
        tree.column('tanggal_diambil', width=100, anchor='center')
        tree.heading('jenis', text='Jenis')
        tree.column('jenis', width=150, anchor='center')
        tree.heading('berat(kg)', text='Berat (kg)')
        tree.column('berat(kg)', width=80, anchor='center')
        tree.heading('harga(kg)', text='Harga (kg)')
        tree.column('harga(kg)', width=80, anchor='center')
        tree.heading('total', text='Total')
        tree.column('total', width=80, anchor='center')
        tree.heading('status', text='Status')
        tree.column('status', width=100, anchor='center')
        
        tree.pack(fill='both', expand=True)

        def cari_pesanan(no_hp):
            try:
                df_nota = pd.read_csv(nota_file)
                df_nota['NomorHP'] = df_nota['NomorHP'].astype(str)  # Pastikan kolom NomorHP adalah string
                filtered_df = df_nota[(df_nota['NomorHP'] == no_hp) & (df_nota['status'] == 'belum selesai')]
                if not filtered_df.empty:
                    display_pesanan(filtered_df)
                else:
                    tree.delete(*tree.get_children())  # Clear the treeview if no data found
                    messagebox.showinfo("Hasil Pencarian", "Data tidak ditemukan atau semua pesanan sudah selesai.")
            except FileNotFoundError:
                messagebox.showerror("Error", "File tidak ditemukan.")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

        def display_pesanan(filtered_df):
            # Clear existing rows in the treeview
            for item in tree.get_children():
                tree.delete(item)
            
            # Insert data into the treeview
            for _, row in filtered_df.iterrows():
                tree.insert('', tk.END, values=row.tolist())

        def centang_selesai():
            no_hp = entry_no_hp.get()
            try:
                df_nota = pd.read_csv(nota_file)
                df_nota['NomorHP'] = df_nota['NomorHP'].astype(str)  # Pastikan kolom NomorHP adalah string
                filtered_df = df_nota[(df_nota['NomorHP'] == no_hp) & (df_nota['status'] == 'belum selesai')]

                for selected_item in tree.selection():
                    item = tree.item(selected_item)
                    item_id = item['values'][0]
                    df_nota.loc[df_nota['id'] == item_id, 'status'] = 'selesai'

                df_nota.to_csv(nota_file, index=False)
                messagebox.showinfo("Status", "Status pesanan berhasil diubah menjadi selesai.")
                # Refresh the data
                cari_pesanan(no_hp)

            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan data: {e}")

        tk.Button(ubah_status_frame, text="Ubah Status Menjadi Selesai", command=centang_selesai, font=("Arial", 16)).pack(pady=10)
        tk.Button(ubah_status_frame, text="Kembali", command=lambda: [ubah_status_frame.destroy(), edit_data()], font=("Arial", 16)).pack(pady=10)

    def edit_data_jasa():
        edit_data_frame.destroy()
        edit_jasa_frame = tk.Frame(root)
        edit_jasa_frame.pack(expand=True)

        # Create a Treeview to display the table
        columns = ['id', 'jenis', 'lama pengerjaan', 'harga']
        tree = ttk.Treeview(edit_jasa_frame, columns=columns, show='headings')
        tree.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='nsew')

        # Define headings
        tree.heading('id', text='ID')
        tree.heading('jenis', text='Jenis')
        tree.heading('lama pengerjaan', text='Lama Pengerjaan')
        tree.heading('harga', text='Harga')

        # Define column widths
        tree.column('id', width=50, anchor='center')
        tree.column('jenis', width=200, anchor='center')
        tree.column('lama pengerjaan', width=150, anchor='center')
        tree.column('harga', width=100, anchor='center')

        # Add data to the treeview
        try:
            df_jasa = pd.read_csv(jasa_file)
            for index, row in df_jasa.iterrows():
                tree.insert('', tk.END, values=(row['id'], row['jenis'], row['lama pengerjaan'], row['harga']))
        except FileNotFoundError:
            messagebox.showerror("Error", "Data layanan tidak ditemukan!")

        tk.Label(edit_jasa_frame, text="ID:", font=("Arial", 16)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        entry_id = tk.Entry(edit_jasa_frame, font=("Arial", 16))
        entry_id.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(edit_jasa_frame, text="Jenis:", font=("Arial", 16)).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        entry_jenis = tk.Entry(edit_jasa_frame, font=("Arial", 16))
        entry_jenis.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(edit_jasa_frame, text="Lama Pengerjaan:", font=("Arial", 16)).grid(row=3, column=0, padx=10, pady=5, sticky='w')
        entry_lama = tk.Entry(edit_jasa_frame, font=("Arial", 16))
        entry_lama.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(edit_jasa_frame, text="Harga:", font=("Arial", 16)).grid(row=4, column=0, padx=10, pady=5, sticky='w')
        entry_harga = tk.Entry(edit_jasa_frame, font=("Arial", 16))
        entry_harga.grid(row=4, column=1, padx=10, pady=5)

        def select_item(event):
            selected_item = tree.selection()[0]
            values = tree.item(selected_item, 'values')
            entry_id.delete(0, tk.END)
            entry_id.insert(0, values[0])
            entry_jenis.delete(0, tk.END)
            entry_jenis.insert(0, values[1])
            entry_lama.delete(0, tk.END)
            entry_lama.insert(0, values[2])
            entry_harga.delete(0, tk.END)
            entry_harga.insert(0, values[3])

        tree.bind('<<TreeviewSelect>>', select_item)

        def update_jasa():
            jasa_id = entry_id.get()
            jenis = entry_jenis.get()
            lama = entry_lama.get()
            harga = entry_harga.get()
            
            try:
                df_jasa = pd.read_csv(jasa_file)
                df_jasa.loc[df_jasa['id'] == int(jasa_id), ['jenis', 'lama pengerjaan', 'harga']] = [jenis, lama, harga]
                df_jasa.to_csv(jasa_file, index=False)
                messagebox.showinfo("Edit Data Jasa", "Data jasa berhasil diubah.")
                edit_jasa_frame.destroy()
                edit_data()
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan data: {e}")

        tk.Button(edit_jasa_frame, text="Update", command=update_jasa, font=("Arial", 16)).grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(edit_jasa_frame, text="Kembali", command=lambda: [edit_jasa_frame.destroy(), edit_data()], font=("Arial", 16)).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def tambah_data_jasa():
        edit_data_frame.destroy()
        tambah_data_jasa_frame = tk.Frame(root)
        tambah_data_jasa_frame.pack(expand=True)

        tk.Label(tambah_data_jasa_frame, text="Tambah Data Jasa", font=("Arial", 24)).pack(pady=10)
        
        tk.Label(tambah_data_jasa_frame, text="Jenis Jasa:", font=("Arial", 16)).pack(pady=5)
        entry_jenis = tk.Entry(tambah_data_jasa_frame, font=("Arial", 16))
        entry_jenis.pack(pady=5)
        
        tk.Label(tambah_data_jasa_frame, text="Lama Pengerjaan (hari):", font=("Arial", 16)).pack(pady=5)
        entry_lama = tk.Entry(tambah_data_jasa_frame, font=("Arial", 16))
        entry_lama.pack(pady=5)
        
        tk.Label(tambah_data_jasa_frame, text="Harga (per kg):", font=("Arial", 16)).pack(pady=5)
        entry_harga = tk.Entry(tambah_data_jasa_frame, font=("Arial", 16))
        entry_harga.pack(pady=5)

        def save_jasa():
            jenis = entry_jenis.get()
            lama = entry_lama.get()
            harga = entry_harga.get()
            
            try:
                if os.path.exists(jasa_file):
                    df = pd.read_csv(jasa_file)
                    last_id = int(df['id'].iloc[-1]) 
                    new_id = last_id + 1 
                else:
                    new_id = 1
    
                new_entry = pd.DataFrame([[new_id, jenis, lama, harga]], columns=['id', 'jenis', 'lama pengerjaan', 'harga'])
                if os.path.exists(jasa_file):
                    df = pd.read_csv(jasa_file)
                    df = pd.concat([df, new_entry], ignore_index=True)
                else:
                    df = new_entry
                
                df.to_csv(jasa_file, index=False)
                messagebox.showinfo("Tambah Data Jasa", "Data jasa berhasil ditambahkan.")
                tambah_data_jasa_frame.destroy()
                edit_data()
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan data: {e}")
        
        tk.Button(tambah_data_jasa_frame, text="Simpan", command=save_jasa, font=("Arial", 16)).pack(pady=5)
        tk.Button(tambah_data_jasa_frame, text="Kembali", command=lambda: [tambah_data_jasa_frame.destroy(), edit_data()], font=("Arial", 16)).pack(pady=5)

    tk.Label(edit_data_frame, text="Edit Data", font=("Arial", 24)).pack(pady=10)

    tk.Button(edit_data_frame, text="Ubah Status Pesanan", command=ubah_status_pesanan, font=("Arial", 16)).pack(pady=5)
    tk.Button(edit_data_frame, text="Edit Data Jasa", command=edit_data_jasa, font=("Arial", 16)).pack(pady=5)
    tk.Button(edit_data_frame, text="Tambah Data Jasa", command=tambah_data_jasa, font=("Arial", 16)).pack(pady=5)
    tk.Button(edit_data_frame, text="Kembali", command=lambda: [edit_data_frame.destroy(), show_menu()], font=("Arial", 16)).pack(pady=5)



# Cari Data function

def submenucaridata():
    # Clear the root frame before adding new widgets
    for widget in root.winfo_children():
        widget.destroy()
    
    cari_data_frame = tk.Frame(root)
    cari_data_frame.pack(expand=True)

    tk.Label(cari_data_frame, text="Cari Data", font=("Arial", 24)).pack(pady=10)

    tk.Button(cari_data_frame, text="Cari Data Berdasarkan Nomor HP", command=cari_data, font=("Arial", 16)).pack(pady=5)
    tk.Button(cari_data_frame, text="Tampilkan Data Nota", command=tampilkan_data_nota, font=("Arial", 16)).pack(pady=5)
    tk.Button(cari_data_frame, text="Kembali", command=lambda: [cari_data_frame.destroy(), show_menu()], font=("Arial", 16)).pack(pady=5)

def cari_data():
    # Clear the root frame before adding new widgets
    for widget in root.winfo_children():
        widget.destroy()
    
    cari_data_frame = tk.Frame(root)
    cari_data_frame.pack(expand=True)

    input_frame = tk.Frame(cari_data_frame)
    input_frame.pack(pady=20)

    tk.Label(input_frame, text="Masukkan Nomor HP:", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=5)
    entry_no_hp = tk.Entry(input_frame, font=("Arial", 16))
    entry_no_hp.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(input_frame, text="Cari", command=lambda: search_by_hp(entry_no_hp.get()), font=("Arial", 16)).grid(row=0, column=2, padx=10, pady=5)

    # Create a Treeview with a scrollbar
    tree_frame = tk.Frame(cari_data_frame)
    tree_frame.pack(padx=10, pady=5, fill='both', expand=True)
    columns = ['ID', 'Nama Pelanggan', 'Nomor HP', 'Tanggal Masuk', 'Tanggal Diambil', 'Jenis', 'Berat (kg)', 'Harga (kg)', 'Total', 'Status']
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="extended")
    
    # Add a vertical scrollbar
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)
    
    # Adjust column widths to fit all columns within the screen width
    column_widths = {
        'ID': 50,
        'Nama Pelanggan': 150,
        'Nomor HP': 100,
        'Tanggal Masuk': 100,
        'Tanggal Diambil': 100,
        'Jenis': 150,
        'Berat (kg)': 80,
        'Harga (kg)': 80,
        'Total': 80,
        'Status': 100
    }
    
    # Add columns and headers to the treeview with adjusted widths
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=column_widths[col], anchor='center')
    
    tree.pack(fill='both', expand=True)

    def search_by_hp(no_hp):
        try:
            df = pd.read_csv(nota_file)
            df['NomorHP'] = df['NomorHP'].astype(str)  # Pastikan kolom NomorHP adalah string
            filtered_df = df[df['NomorHP'] == no_hp]
            if not filtered_df.empty:
                display_search_results(filtered_df)
            else:
                tree.delete(*tree.get_children())  # Clear the treeview if no data found
                messagebox.showinfo("Hasil Pencarian", "Data tidak ditemukan.")
        except FileNotFoundError:
            messagebox.showerror("Error", "File tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def display_search_results(filtered_df):
        # Clear existing rows in the treeview
        for item in tree.get_children():
            tree.delete(item)
        
        # Insert data into the treeview
        for _, row in filtered_df.iterrows():
            tree.insert('', tk.END, values=row.tolist())

    tk.Button(cari_data_frame, text="Kembali", command=lambda: [cari_data_frame.destroy(), submenucaridata()], font=("Arial", 16)).pack(pady=5)

def tampilkan_data_nota():
    # Clear the root frame before adding new widgets
    for widget in root.winfo_children():
        widget.destroy()
    
    tampilkan_data_frame = tk.Frame(root)
    tampilkan_data_frame.pack(expand=True)

    # Create a Treeview with a scrollbar
    tree_frame = tk.Frame(tampilkan_data_frame)
    tree_frame.pack(padx=10, pady=5, fill='both', expand=True)
    columns = ['ID', 'Nama Pelanggan', 'Nomor HP', 'Tanggal Masuk', 'Tanggal Diambil', 'Jenis', 'Berat (kg)', 'Harga (kg)', 'Total', 'Status']
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="extended")
    
    # Add a vertical scrollbar
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)
    
    # Adjust column widths to fit all columns within the screen width
    column_widths = {
        'ID': 50,
        'Nama Pelanggan': 150,
        'Nomor HP': 100,
        'Tanggal Masuk': 100,
        'Tanggal Diambil': 100,
        'Jenis': 150,
        'Berat (kg)': 80,
        'Harga (kg)': 80,
        'Total': 80,
        'Status': 100
    }
    
    # Add columns and headers to the treeview with adjusted widths
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=column_widths[col], anchor='center')
    
    tree.pack(fill='both', expand=True)

    def display_sorted_data(filtered_df):
        # Clear existing rows in the treeview
        for item in tree.get_children():
            tree.delete(item)
        
        # Insert data into the treeview
        for _, row in filtered_df.iterrows():
            tree.insert('', tk.END, values=row.tolist())

    try:
        df = pd.read_csv(nota_file)
        df['tanggal_diambil'] = pd.to_datetime(df['tanggal_diambil'])
        df = df[df['status'] == 'belum selesai']
        df = df.sort_values(by='tanggal_diambil')
        display_sorted_data(df)
    except FileNotFoundError:
        messagebox.showerror("Error", "File tidak ditemukan.")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    tk.Button(tampilkan_data_frame, text="Kembali", command=lambda: [tampilkan_data_frame.destroy(), submenucaridata()], font=("Arial", 16)).pack(pady=5)
# Exit function
def keluar():
    if messagebox.askyesno("Keluar", "Apakah Anda yakin ingin keluar?"):
        root.quit()

# Show Menu function
def show_menu():
    menu_frame = tk.Frame(root)
    menu_frame.pack(expand=True)

    tk.Label(menu_frame, text="Menu", font=("Arial", 24)).pack(pady=10)

    tk.Button(menu_frame, text="Input Data", command=lambda: [menu_frame.destroy(), input_data()], font=("Arial", 16)).pack(pady=5)
    tk.Button(menu_frame, text="Edit Data", command=lambda: [menu_frame.destroy(), edit_data()], font=("Arial", 16)).pack(pady=5)
    tk.Button(menu_frame, text="Cari Data", command=lambda: [menu_frame.destroy(), submenucaridata()], font=("Arial", 16)).pack(pady=5)
    tk.Button(menu_frame, text="Keluar", command=keluar, font=("Arial", 16)).pack(pady=5)


# Welcome Page function
def welcome_page():
    welcome_frame = tk.Frame(root)
    welcome_frame.pack(expand=True)

    tk.Label(welcome_frame, text="Selamat Datang di Aplikasi Managemen Laundry", font=("Arial", 24)).pack(pady=10)

    tk.Button(welcome_frame, text="Sign In", command=lambda: [welcome_frame.destroy(), sign_in()], font=("Arial", 16)).pack(pady=5)
    tk.Button(welcome_frame, text="Sign Up", command=lambda: [welcome_frame.destroy(), sign_up()], font=("Arial", 16)).pack(pady=5)
    

# Main function
def main():
    global root
    root = tk.Tk()
    root.title("Aplikasi Managemen Laundry")
    root.state('zoomed')

    welcome_page()

    root.mainloop()

if __name__ == "__main__":
    main()
