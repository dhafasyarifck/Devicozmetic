import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import plotly.express as px  # Library untuk plotly express

# Fungsi untuk membaca file CSV
def read_csv_file(file):
    df = pd.read_csv(file)
    return df

# Fungsi untuk menentukan barang laris atau tidak laris
def determine_popularity(df, threshold_jumlah, threshold_harga):
    # Menghitung beberapa fitur relevan
    df['Total Diskon'] = pd.to_numeric(df['Total Diskon'], errors='coerce').fillna(0)
    df['Diskon Dari Penjual'] = pd.to_numeric(df['Diskon Dari Penjual'], errors='coerce').fillna(0)
    df['Harga Setelah Diskon'] = pd.to_numeric(df['Harga Setelah Diskon'], errors='coerce').fillna(0)
    df['Total Harga Produk'] = pd.to_numeric(df['Total Harga Produk'], errors='coerce').fillna(0)
    
    penjualan_produk = df.groupby('Nama_Produk').agg({
        'Jumlah_Penjualan': 'sum',
        'Harga_Awal': 'mean',
        'Total Diskon': 'mean',
        'Diskon Dari Penjual': 'mean',
        'Harga Setelah Diskon': 'mean',
        'Total Harga Produk': 'mean'
    }).reset_index()
    
    # Tentukan barang laris atau tidak laris berdasarkan threshold yang dipilih
    penjualan_produk['Status'] = np.where(
        (penjualan_produk['Jumlah_Penjualan'] >= threshold_jumlah) & 
        (penjualan_produk['Harga_Awal'] >= threshold_harga),
        'Laris', 'Tidak Laris'
    )
    
    return penjualan_produk

# Fungsi untuk menyimpan hasil ke database MySQL
def save_to_db(df, penjualan_produk):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='devicozmetic'  # Ganti dengan nama database Anda
        )
        cursor = conn.cursor()
        
        # Buat tabel jika belum ada
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analisis_barang (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama_produk VARCHAR(255) UNIQUE,
                jumlah_penjualan INT,
                harga_awal FLOAT,
                total_diskon FLOAT,
                diskon_dari_penjual FLOAT,
                harga_setelah_diskon FLOAT,
                total_harga_produk FLOAT,
                status VARCHAR(10)
            )
        """)
        
        # Masukkan data ke dalam tabel
        for idx, row in penjualan_produk.iterrows():
            cursor.execute("""
                INSERT INTO analisis_barang (nama_produk, jumlah_penjualan, harga_awal, total_diskon, diskon_dari_penjual, harga_setelah_diskon, total_harga_produk, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    jumlah_penjualan=VALUES(jumlah_penjualan),
                    harga_awal=VALUES(harga_awal),
                    total_diskon=VALUES(total_diskon),
                    diskon_dari_penjual=VALUES(diskon_dari_penjual),
                    harga_setelah_diskon=VALUES(harga_setelah_diskon),
                    total_harga_produk=VALUES(total_harga_produk),
                    status=VALUES(status)
            """, (row['Nama_Produk'], row['Jumlah_Penjualan'], row['Harga_Awal'], row['Total Diskon'], row['Diskon Dari Penjual'], row['Harga Setelah Diskon'], row['Total Harga Produk'], row['Status']))

        conn.commit()
        st.success("Data berhasil disimpan ke database!")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Tampilan aplikasi Streamlit
def show_halaman_datapenjualan():
    st.title('Analisis Barang Laris dengan Streamlit')
    
    # Upload multiple file CSV
    st.sidebar.title('Upload File CSV')
    uploaded_files = st.sidebar.file_uploader("Unggah file CSV", type=['csv'], accept_multiple_files=True)
    
    if uploaded_files:
        for file in uploaded_files:
            # Baca data dari file CSV
            df = read_csv_file(file)
            
            # Tampilkan nama file dan data penjualan
            st.subheader(f'Data Penjualan dari File: {file.name}')
            st.write(df)
            
            # Handle missing values and compute max values
            max_jumlah = int(df['Jumlah_Penjualan'].max() if not pd.isnull(df['Jumlah_Penjualan']).all() else 0)
            max_harga = float(df['Harga_Awal'].max() if not pd.isnull(df['Harga_Awal']).all() else 0.0)
            
            # Kontrol untuk memilih nilai threshold
            st.sidebar.subheader('Pilih Threshold')
            threshold_jumlah = st.sidebar.slider('Threshold Jumlah Penjualan', min_value=0, max_value=max_jumlah, value=int(np.median(df['Jumlah_Penjualan'].fillna(0))))
            threshold_harga = st.sidebar.slider('Threshold Harga_Awal', min_value=0.0, max_value=max_harga, value=np.median(df['Harga_Awal'].fillna(0.0)))
            
            # Analisis untuk menentukan barang laris atau tidak laris
            penjualan_produk = determine_popularity(df, threshold_jumlah, threshold_harga)
            
            # Hitung jumlah barang berstatus "Laris" dan "Tidak Laris"
            count_laris = penjualan_produk[penjualan_produk['Status'] == 'Laris'].shape[0]
            count_tidak_laris = penjualan_produk[penjualan_produk['Status'] == 'Tidak Laris'].shape[0]
            
            # Tampilkan tabel barang laris atau tidak laris
            st.subheader(f'Status Barang dari File: {file.name} (Laris/Tidak Laris)')
            st.write(penjualan_produk)
            
            # Tampilkan jumlah barang laris dan tidak laris
            st.subheader('Total Barang')
            st.write(f'Barang Laris: {count_laris}')
            st.write(f'Barang Tidak Laris: {count_tidak_laris}')
            
            # Tombol untuk menyimpan dataset ke database
            if st.button(f"Simpan ke Database {file.name}"):
                save_to_db(df, penjualan_produk)
            
           # Visualisasi data dengan Pie Chart
            fig = px.pie(penjualan_produk, names='Status', title=f'Proporsi Barang Laris/Tidak Laris dari File: {file.name}', 
                        labels={'Status': 'Status Barang'})
            st.plotly_chart(fig)

if __name__ == '__main__':
    show_halaman_datapenjualan()
