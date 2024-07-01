# app.py

import streamlit as st
import mysql.connector
from admin import admin_panel
from pemilik_toko import pemilik_toko_panel

# Koneksi ke database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="devicozmetic"
)
cursor = conn.cursor()

# Streamlit UI untuk aplikasi utama
def main():
    st.title("Aplikasi Devicozmetics")

    # Cek status login
    if "username" not in st.session_state:
        login_form()
    else:
        level = st.session_state["level"]
        if level == 'admin':
            admin_panel()  # Panggil fungsi admin_panel() dari admin.py
        elif level == 'Pemilik_toko':
            pemilik_toko_panel()  # Panggil fungsi pemilik_toko_panel() dari pemilik_toko.py

def login_form():
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        result = cursor.fetchone()
        if result:
            level = result[2]
            st.session_state["username"] = username
            st.session_state["level"] = level
            st.success(f"Logged in as {username}")
            st.write(f"Level Akses: {level}")
            redirect_to_page(level)
        else:
            st.error("Invalid credentials")

def redirect_to_page(level):
    # Redirect halaman berdasarkan level akses
    if level == 'admin':
        admin_panel()
    elif level == 'Pemilik_toko':
        pemilik_toko_panel()
    else:
        st.error("Level akses tidak valid")

# Panggil fungsi main
if __name__ == "__main__":
    main()
