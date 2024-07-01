import streamlit as st
import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='devicozmetic'
    )
    return conn

def create_user(username, password, level):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, level) VALUES (%s, %s, %s)", (username, password, level))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("User berhasil ditambahkan!")

def read_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def update_user(user_id, username, password, level):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username=%s, password=%s, level=%s WHERE id=%s", (username, password, level, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("User berhasil diperbarui!")

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("User berhasil dihapus!")

def show_halaman_users():
    st.title("Data Users")
    
    menu = ["Create", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Create":
        st.subheader("Tambah User")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        level = st.selectbox("Level", ["admin", "Pemilik_toko"])
        if st.button("Tambah"):
            create_user(username, password, level)
    
    elif choice == "Read":
        st.subheader("Daftar Users")
        users = read_users()
        for user in users:
            st.write(f"ID: {user[0]}, Username: {user[1]}, Level: {user[3]}")
    
    elif choice == "Update":
        st.subheader("Perbarui User")
        users = read_users()
        user_id = st.selectbox("Pilih User untuk Diperbarui", [user[0] for user in users])
        user = next(user for user in users if user[0] == user_id)
        username = st.text_input("Username", user[1])
        password = st.text_input("Password", user[2], type='password')
        level = st.selectbox("Level", ["admin", "Pemilik_toko"], index=0 if user[3] == "admin" else 1)
        if st.button("Perbarui"):
            update_user(user_id, username, password, level)
    
    elif choice == "Delete":
        st.subheader("Hapus User")
        users = read_users()
        user_id = st.selectbox("Pilih User untuk Dihapus", [user[0] for user in users])
        if st.button("Hapus"):
            delete_user(user_id)

# Panggil fungsi untuk menampilkan halaman users
show_halaman_users()
