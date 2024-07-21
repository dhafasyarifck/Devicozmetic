import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# Fungsi untuk koneksi ke database MySQL
def connect_to_db():
    """
    Membuat koneksi ke database MySQL.
    """
    return mysql.connector.connect(
            host="sql12.freemysqlhosting.net",
            user="sql12721204",
            password="t4itLMeUj2",
            database="sql12721204" 
    )

# Fungsi untuk membaca data dari tabel analisis_barang
def read_analisis_barang(conn):
    """
    Membaca data dari tabel 'analisis_barang'.
    Args:
    conn (mysql.connector.connection.MySQLConnection): Objek koneksi database.

    Returns:
    pd.DataFrame: DataFrame yang berisi data dari 'analisis_barang'.
    """
    query = "SELECT * FROM analisis_barang"
    df = pd.read_sql(query, conn)
    return df

# Fungsi untuk membaca data dari tabel hasil_prediksi
def read_hasil_prediksi(conn):
    """
    Membaca data dari tabel 'prediksi'.
    Args:
    conn (mysql.connector.connection.MySQLConnection): Objek koneksi database.

    Returns:
    pd.DataFrame: DataFrame yang berisi data dari 'prediksi'.
    """
    query = "SELECT * FROM prediksi"
    df = pd.read_sql(query, conn)
    return df

# Fungsi untuk membaca data dari tabel history_model
def read_history_model(conn):
    """
    Membaca data dari tabel 'history_model'.
    Args:
    conn (mysql.connector.connection.MySQLConnection): Objek koneksi database.

    Returns:
    pd.DataFrame: DataFrame yang berisi data dari 'history_model'.
    """
    query = "SELECT * FROM history_model"
    df = pd.read_sql(query, conn)
    return df

# Fungsi untuk menampilkan dashboard grafik
def show_halaman_utama():
    """
    Menampilkan dashboard utama dengan visualisasi analisis produk dan hasil prediksi.
    """
    st.title("DeviCozmetic Halaman Utama")
    st.write("Selamat datang di halaman utama!")
    
    # Koneksi ke database
    try:
        conn = connect_to_db()
        
        # Baca data dari tabel-tabel yang diperlukan
        df_analisis_barang = read_analisis_barang(conn)
        df_hasil_prediksi = read_hasil_prediksi(conn)
        df_history_model = read_history_model(conn)
        
        # Visualisasi data Analisis Barang
        st.header("Grafik Analisis Barang")
        st.write("Grafik ini menunjukkan jumlah penjualan per produk dengan membedakan status barang menggunakan warna yang berbeda.")
        if not df_analisis_barang.empty:
            fig_analisis = px.bar(df_analisis_barang, x='nama_produk', y='jumlah_penjualan', color='status', 
                                  title='Jumlah Penjualan per Produk', labels={'nama_produk': 'Nama Produk', 'jumlah_penjualan': 'Jumlah Penjualan'})
            st.plotly_chart(fig_analisis, use_container_width=True)
        else:
            st.write("Data untuk grafik Analisis Barang tidak tersedia.")
        
        # Visualisasi data Hasil Prediksi
        st.header("Grafik Hasil Prediksi")
        st.write("Grafik ini menampilkan distribusi hasil prediksi dari model dalam bentuk pie chart.")
        
        # Debugging: tampilkan kolom yang tersedia dalam df_hasil_prediksi
        st.write("Kolom-kolom dalam df_hasil_prediksi:")
        st.write(df_hasil_prediksi.columns)
        
        if not df_hasil_prediksi.empty:
            # Pilih kolom yang sesuai untuk pie chart
            if 'predicted_sales' in df_hasil_prediksi.columns:
                fig_prediksi = px.pie(df_hasil_prediksi, names='predicted_sales', title='Distribusi Hasil Prediksi')
            else:
                st.write("Kolom 'predicted_sales' tidak ditemukan dalam data hasil prediksi.")
                fig_prediksi = px.pie(df_hasil_prediksi, names=df_hasil_prediksi.columns[0], title='Distribusi Hasil Prediksi')
            
            st.plotly_chart(fig_prediksi, use_container_width=True)
        else:
            st.write("Data untuk grafik Hasil Prediksi tidak tersedia.")
    
    except Exception as e:
        st.error(f"Terjadi kesalahan saat menghubungkan ke database atau mengambil data: {e}")
    
    finally:
        if conn.is_connected():
            conn.close()

# Panggil fungsi utama untuk menjalankan aplikasi
if __name__ == '__main__':
    show_halaman_utama()
