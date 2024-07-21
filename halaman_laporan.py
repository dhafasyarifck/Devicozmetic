import streamlit as st
import pandas as pd
import mysql.connector
import base64
# Fungsi untuk koneksi ke database MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="sql12.freemysqlhosting.net",
        user="sql12721204",
        password="t4itLMeUj2",
        database="sql12721204" 
    )

# Fungsi untuk membaca data dari tabel analisis_barang
def read_analisis_barang(conn):
    query = "SELECT * FROM analisis_barang"
    df = pd.read_sql(query, conn)
    return df

# Fungsi untuk membaca data dari tabel hasil_prediksi
def read_hasil_prediksi(conn):
    query = "SELECT * FROM prediksi"
    df = pd.read_sql(query, conn)
    return df

# Fungsi untuk membaca data dari tabel history_model
def read_history_model(conn):
    query = "SELECT * FROM history_model"
    df = pd.read_sql(query, conn)
    return df

# Fungsi untuk menampilkan halaman laporan
def show_halaman_laporan():
    st.title("Halaman Laporan")
    
    # Koneksi ke database
    conn = connect_to_db()
    
    # Baca data dari tabel-tabel yang diperlukan
    df_analisis_barang = read_analisis_barang(conn)
    df_hasil_prediksi = read_hasil_prediksi(conn)
    df_history_model = read_history_model(conn)
    
    # Tampilkan data dalam bentuk tabel di Streamlit
    st.subheader("Tabel Analisis Penjualan")
    st.dataframe(df_analisis_barang)

    st.subheader("Tabel Hasil Prediksi")
    st.dataframe(df_hasil_prediksi)

    st.subheader("Tabel History Model")
    st.dataframe(df_history_model)

    # Tombol untuk mengunduh data dalam format Excel
    def download_excel(df, filename):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} as CSV</a>'
        return href

    st.subheader("Unduh Data sebagai Excel")
    st.markdown(download_excel(df_analisis_barang, "analisis_barang"), unsafe_allow_html=True)
    st.markdown(download_excel(df_hasil_prediksi, "hasil_prediksi"), unsafe_allow_html=True)
    st.markdown(download_excel(df_history_model, "history_model"), unsafe_allow_html=True)

# Panggil fungsi main untuk menjalankan aplikasi
if __name__ == '__main__':
    show_halaman_laporan()
