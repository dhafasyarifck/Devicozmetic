# admin.py

import streamlit as st
from streamlit_option_menu import option_menu
import urllib.parse
import halaman_utama
import halaman_users
import halaman_prediksi
import halaman_laporan
import halaman_trainingmodel
import halaman_datapenjualan

def admin_panel():
    
    # Menu utama
    selected = option_menu(
        menu_title=None,
        options=["Home", "Data Users", "Data Penjualan", "Training Model", "Data Prediksi", "Laporan", "Logout"],
        icons=["house", "graph-up-arrow", "box", "box", "file-earmark-bar-graph", "file-earmark-check", "arrow-right-square"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )
 
    

    # Tampilkan halaman sesuai pilihan di menu utama
    if selected == "Home":
        halaman_utama.show_halaman_utama()
    
    elif selected == "Data Users":
        halaman_users.show_halaman_users()

    elif selected == "Data Penjualan":
        halaman_datapenjualan.show_halaman_datapenjualan()
    
    elif selected == "Data Prediksi":
        halaman_prediksi.show_halaman_prediksi()
    
    elif selected == "Laporan":
        halaman_laporan.show_halaman_laporan()
    
    elif selected == "Training Model":
        halaman_trainingmodel.show_halaman_trainingmodel()
    elif selected == "Logout":
        st.session_state.clear()  # Hapus semua session state
        st.experimental_rerun()  # Rer

   
