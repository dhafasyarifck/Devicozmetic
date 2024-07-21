import streamlit as st
import mysql.connector
from mysql.connector import Error
from admin import admin_panel
from pemilik_toko import pemilik_toko_panel

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="sql111.infinityfree.com",
            user="if0_36944061",
            password="SZ9Q2OQu9Lk83p",
            database="if0_36944061_devicozmetic"
        )
        if conn.is_connected():
            st.session_state["conn"] = conn
            st.session_state["cursor"] = conn.cursor()
            return conn
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Streamlit UI untuk aplikasi utama
def main():
    st.title("Aplikasi Devicozmetics")
    st.write("Aplikasi Ini Memproses Data Penjualan Devicozmetic Lalu Memprediksi Produk Yang Paling Diminati")

    # Cek status login
    if "conn" not in st.session_state:
        conn = create_connection()
        if conn is None:
            st.stop()

    if "username" not in st.session_state:
        login_form()
        registration_form()  # Tampilkan form registrasi jika belum login
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
        try:
            cursor = st.session_state["cursor"]
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
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
        except Error as e:
            st.error(f"Error executing query: {e}")

def registration_form():
    st.subheader("Registration")

    reg_username = st.text_input("Username", key="reg_username")
    reg_password = st.text_input("Password", type="password", key="reg_password")
    reg_level = st.selectbox("Level Akses", ["admin", "Pemilik_toko"], key="reg_level")

    if st.button("Register"):
        try:
            cursor = st.session_state["cursor"]
            cursor.execute("SELECT * FROM users WHERE username=%s", (reg_username,))
            if cursor.fetchone():
                st.error("Username already exists")
            else:
                insert_query = "INSERT INTO users (username, password, level) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (reg_username, reg_password, reg_level))
                st.session_state["conn"].commit()
                st.success(f"User {reg_username} registered successfully with level {reg_level}")
        except Error as e:
            st.error(f"Error executing query: {e}")

def redirect_to_page(level):
    if level == 'admin':
        admin_panel()
    elif level == 'Pemilik_toko':
        pemilik_toko_panel()
    else:
        st.error("Invalid access level")

if __name__ == "__main__":
    main()
