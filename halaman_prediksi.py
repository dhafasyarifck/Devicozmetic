import streamlit as st
import pandas as pd
import joblib
import mysql.connector
from datetime import date
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

# Load the SVM and Decision Tree models
svm_model = joblib.load('svm_model.joblib')
dt_model = joblib.load('decision_tree_model.joblib')

# Fungsi untuk menyimpan hasil prediksi ke dalam tabel hasil_prediksi di database MySQL
def save_prediction_to_db(jumlah_penjualan, harga_awal, total_diskon, diskon_dari_penjual, svm_prediction, dt_prediction, conn):
    try:
        cursor = conn.cursor()
        today = date.today().isoformat()
        cursor.execute("""
            INSERT INTO hasil_prediksi 
            (tanggal_prediksi, jumlah_penjualan, harga_awal, total_diskon, diskon_dari_penjual, prediksi_svm, prediksi_decision_tree) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (today, jumlah_penjualan, harga_awal, total_diskon, diskon_dari_penjual, svm_prediction, dt_prediction))
        conn.commit()
        cursor.close()
        st.success("Hasil prediksi berhasil disimpan ke dalam database.")
    except Exception as e:
        st.error(f"Error: {e}")

# Fungsi untuk menampilkan halaman prediksi produk
def show_data_prediksi_produk(conn):
    st.subheader("Data Prediksi Produk")
    st.write("Isi data untuk diprediksi:")
    jumlah_penjualan = st.number_input("Jumlah Penjualan")
    harga_awal = st.number_input("Harga Awal")
    total_diskon = st.number_input("Total Diskon")
    diskon_dari_penjual = st.number_input("Diskon Dari Penjual")
    
    # Tombol untuk memicu prediksi
    if st.button("Predict"):
        # Membuat DataFrame dari data baru
        new_data = {'Jumlah_Penjualan': [jumlah_penjualan], 
                    'Harga_Awal': [harga_awal], 
                    'Total Diskon': [total_diskon], 
                    'Diskon Dari Penjual': [diskon_dari_penjual]}
        new_data_df = pd.DataFrame(new_data)
        
        # Prediksi dengan model SVM
        svm_prediction = svm_model.predict(new_data_df)
        
        # Prediksi dengan model Decision Tree
        dt_prediction = dt_model.predict(new_data_df)
        
        st.subheader("Hasil Prediksi")
        st.write("Prediksi SVM:", svm_prediction[0])
        st.write("Prediksi Decision Tree:", dt_prediction[0])
        
        # Simpan hasil prediksi ke dalam database
        save_prediction_to_db(jumlah_penjualan, harga_awal, total_diskon, diskon_dari_penjual, svm_prediction[0], dt_prediction[0], conn)

# Fungsi utama untuk menampilkan halaman prediksi produk
def show_halaman_prediksi():
    st.title("Halaman Prediksi Produk")
    
    # Koneksi ke database MySQL
    conn = mysql.connector.connect(
       host="sql12.freemysqlhosting.net",
            user="sql12721204",
            password="t4itLMeUj2",
            database="sql12721204"
    )
    
    show_data_prediksi_produk(conn)

# Panggil fungsi main untuk menjalankan aplikasi
if __name__ == '__main__':
    show_halaman_prediksi()
