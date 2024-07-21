import streamlit as st
import pandas as pd

# Title of the application
st.title("Simple Streamlit App")

# Sidebar for navigation
menu = ["Home", "Data", "About"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Home")
    st.write("Welcome to the simple Streamlit app.")

elif choice == "Data":
    st.subheader("Data")
    
    # Sample data
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [24, 27, 22, 32],
        'City': ['New York', 'San Francisco', 'Los Angeles', 'Chicago']
    }
    df = pd.DataFrame(data)
    
    st.write("Here is some sample data:")
    st.dataframe(df)
    
    # File upload functionality
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Uploaded Data:")
        st.dataframe(data)

elif choice == "About":
    st.subheader("About")
    st.write("This is a simple Streamlit app created for demonstration purposes.")

# Run the app using: streamlit run app.py
