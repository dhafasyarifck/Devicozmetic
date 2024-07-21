import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

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
    query = "SELECT * FROM hasil_prediksi"
    df = pd.read_sql(query, conn)
    return df

# Fungsi untuk membaca data dari tabel history_model
def read_history_model(conn):
    query = "SELECT * FROM history_model"
    df = pd.read_sql(query, conn)
    return df

# Fungsi untuk menampilkan dashboard grafik
def show_halaman_utama():
    st.title("Halaman Utama")
    st.write("Selamat datang di halaman utama!")
    
    # Koneksi ke database
    conn = connect_to_db()
    
    # Baca data dari tabel-tabel yang diperlukan
    df_analisis_barang = read_analisis_barang(conn)
    df_hasil_prediksi = read_hasil_prediksi(conn)
    df_history_model = read_history_model(conn)
    
    # Visualisasi data Analisis Barang
    st.header("Grafik Analisis Barang")
    st.write("Grafik ini menunjukkan jumlah penjualan per produk dengan membedakan status barang menggunakan warna yang berbeda.")
    fig_analisis = px.bar(df_analisis_barang, x='nama_produk', y='jumlah_penjualan', color='status', 
                          title='Jumlah Penjualan per Produk', labels={'nama_produk': 'Nama Produk', 'jumlah_penjualan': 'Jumlah Penjualan'})
    st.plotly_chart(fig_analisis, use_container_width=True)
    
    # Visualisasi data Hasil Prediksi
    st.header("Grafik Hasil Prediksi")
    st.write("Grafik ini menampilkan distribusi hasil prediksi dari model SVM dalam bentuk pie chart.")
    fig_prediksi = px.pie(df_hasil_prediksi, names='prediksi_svm', title='Distribusi Hasil Prediksi SVM')
    st.plotly_chart(fig_prediksi, use_container_width=True)
    
    # Visualisasi data History Model
    st.header("Grafik History Model")
    st.write("Grafik ini menunjukkan history training model berdasarkan tanggal training dan nama model yang digunakan.")
    fig_model = px.line(df_history_model, x='training_date', y='model_name', title='History Training Model')
    st.plotly_chart(fig_model, use_container_width=True)

# Panggil fungsi main untuk menjalankan aplikasi
if __name__ == '__main__':
    show_halaman_utama()
