import streamlit as st
import pandas as pd
import joblib
import mysql.connector
from datetime import date
from io import BytesIO

# Fungsi untuk memuat model terbaru dari tabel history_model di database MySQL
def load_latest_model(conn, model_name):
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT model_binary FROM history_model WHERE model_name = %s ORDER BY training_date DESC LIMIT 1", (model_name,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            model_binary = result['model_binary']
            # Gunakan BytesIO untuk membaca model binary
            model_io = BytesIO(model_binary)
            model = joblib.load(model_io)
            return model
        else:
            st.error(f"Tidak ada model {model_name} ditemukan di history_model.")
            return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Fungsi untuk memprediksi dan menyimpan hasil prediksi ke dalam tabel prediksi
def predict_and_save_data(model, data, product_names, conn, model_name):
    try:
        predictions = model.predict(data)
        product_names['Predicted Sales'] = predictions
        product_names['Status'] = f'Predicted by {model_name}'  # Menambahkan kolom status dengan nama model

        st.subheader("Hasil Prediksi")
        st.write(product_names)

        # Simpan hasil prediksi ke dalam tabel prediksi
        cursor = conn.cursor()
        today = date.today().isoformat()
        for i, row in product_names.iterrows():
            cursor.execute(
                "INSERT INTO prediksi (nama_barang, jumlah_penjualan, harga_awal, total_diskon, rating, total_harga_produk, predicted_sales, prediction_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    row['Nama Barang'], data.iloc[i]['Jumlah_Penjualan'], data.iloc[i]['Harga_Awal'], 
                    data.iloc[i]['Total Diskon'], data.iloc[i]['Rating'], data.iloc[i]['Total Harga Produk'],
                    row['Predicted Sales'], today, row['Status']
                )
            )
        conn.commit()
        cursor.close()

    except Exception as e:
        st.error(f"Error predicting and saving data: {e}")

# Fungsi untuk menampilkan halaman prediksi
def show_halaman_prediksi():
    st.title("Prediksi Barang Baru")

    # Input manual untuk data produk
    nama_barang = st.text_input("Nama Barang")
    jumlah_penjualan = st.number_input("Jumlah Penjualan", min_value=0, value=0)
    harga_awal = st.number_input("Harga Awal", min_value=0.0, value=0.0)
    total_diskon = st.number_input("Total Diskon", min_value=0.0, value=0.0)
    rating = st.number_input("Rating", min_value=0.0, max_value=5.0, value=0.0)
    total_harga_produk = st.number_input("Total Harga Produk", min_value=0.0, value=0.0)

    # Pilih model untuk prediksi
    model_choice = st.selectbox("Pilih Model untuk Prediksi", ["SVM", "Decision Tree"])

    if st.button("Prediksi"):
        # Masukkan data input ke dalam DataFrame
        data = pd.DataFrame({
            'Jumlah_Penjualan': [jumlah_penjualan],
            'Harga_Awal': [harga_awal],
            'Total Diskon': [total_diskon],
            'Rating': [rating],
            'Total Harga Produk': [total_harga_produk]
        })

        product_names = pd.DataFrame({'Nama Barang': [nama_barang]})

        # Koneksi ke database
        conn = mysql.connector.connect(
            host="sql12.freemysqlhosting.net",
            user="sql12721204",
            password="t4itLMeUj2",
            database="sql12721204" 
        )

        # Muat model terbaru
        svm_model = load_latest_model(conn, 'svm_model')
        dt_model = load_latest_model(conn, 'decision_tree_model')

        # Pilih model untuk prediksi
        if model_choice == "SVM":
            selected_model = svm_model
        else:
            selected_model = dt_model

        # Lakukan prediksi dan simpan hasilnya
        if selected_model:
            predict_and_save_data(selected_model, data, product_names, conn, model_choice)
        else:
            st.error("Model belum dimuat.")

# Panggil fungsi untuk menampilkan halaman prediksi
show_halaman_prediksi()
