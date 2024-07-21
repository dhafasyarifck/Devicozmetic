import streamlit as st
import mysql.connector
from admin import admin_panel
from pemilik_toko import pemilik_toko_panel

# Koneksi ke database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Isi dengan password database Anda
    database="devicozmetic"
)
cursor = conn.cursor()

# Streamlit UI untuk aplikasi utama
def main():
    st.title("Aplikasi Devicozmetics")
    st.write("Aplikasi Ini Memproses Data Penjualan Devicozmetic Lalu Memprediksi Produk Yang Paling Diminati")

    # Cek status login
    if "username" not in st.session_state:
        login_form()
        # Tampilkan form registrasi jika belum login
    else:
        level = st.session_state["level"]
        if level == 'admin':
            admin_panel()  # Panggil fungsi admin_panel() dari admin.py
        elif level == 'Pemilik_toko':
            pemilik_toko_panel()  # Panggil fungsi pemilik_toko_panel() dari pemilik_toko.py

def login_form():
    st.subheader("Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        result = cursor.fetchone()
        if result:
            level = result[3]  # Menggunakan indeks 3 karena level akses berada di indeks 3 pada result tuple
            st.session_state["username"] = username
            st.session_state["level"] = level
            st.success(f"Logged in as {username}")
            st.write(f"Level Akses: {level}")
            redirect_to_page(level)
        else:
            st.error("Username dan Password Salah")

def registration_form():
    st.subheader("Registration")

    reg_username = st.text_input("Username", key="reg_username")
    reg_password = st.text_input("Password", type="password", key="reg_password")
    reg_level = st.selectbox("Level Akses", ["admin", "Pemilik_toko"], key="reg_level")

    if st.button("Register"):
        # Periksa apakah username sudah ada
        cursor.execute(f"SELECT * FROM users WHERE username='{reg_username}'")
        if cursor.fetchone():
            st.error("Username already exists")
        else:
            # Tambahkan pengguna baru ke database
            insert_query = f"INSERT INTO users (username, password, level) VALUES ('{reg_username}', '{reg_password}', '{reg_level}')"
            cursor.execute(insert_query)
            conn.commit()
            st.success(f"User {reg_username} registered successfully with level {reg_level}")

def redirect_to_page(level):
    # Redirect halaman berdasarkan level akses
    if level == 'admin':
        admin_panel()
    elif level == 'Pemilik_toko':
        pemilik_toko_panel()
    else:
        st.error("Invalid access level")



# Panggil fungsi main
if __name__ == "__main__":
    main()
