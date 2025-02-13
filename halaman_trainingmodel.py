import streamlit as st
import pandas as pd
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import joblib
import mysql.connector
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import roc_curve, auc

# Fungsi untuk menyimpan model ke dalam tabel history_model di database MySQL
def save_model_to_history(model, model_name, conn):
    try:
        # Serialisasi model ke dalam file
        model_filename = f"{model_name}.joblib"
        joblib.dump(model, model_filename)
        
        # Baca model dari file
        with open(model_filename, 'rb') as f:
            model_binary = f.read()
        
        # Simpan model ke dalam tabel history_model
        cursor = conn.cursor()
        today = date.today().isoformat()
        cursor.execute("INSERT INTO history_model (model_name, training_date, model_binary) VALUES (%s, %s, %s)",
                       (model_name, today, model_binary))
        conn.commit()
        cursor.close()
        
        st.success(f"Model {model_name} berhasil disimpan ke dalam history_model dengan tanggal {today}.")
    except Exception as e:
        st.error(f"Error: {e}")

# Fungsi untuk memprediksi jumlah penjualan dan menampilkan produk paling diminati
def predict_and_show_top_products(model, features_df, product_names):
    try:
        # Prediksi jumlah penjualan
        predictions = model.predict(features_df)
        
        # Tambahkan prediksi ke DataFrame produk
        product_names['Predicted Sales'] = predictions
        
        # Urutkan berdasarkan prediksi jumlah penjualan tertinggi
        top_products = product_names.sort_values(by='Predicted Sales', ascending=False)
        
        # Tampilkan produk paling diminati
        st.subheader("Produk Paling Diminati")
        st.write(top_products)
        
    except Exception as e:
        st.error(f"Error predicting sales: {e}")

# Fungsi untuk menampilkan confusion matrix
def plot_confusion_matrix(cm, title):
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_title(title)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('True')
    st.pyplot(fig)

# Fungsi untuk menampilkan perbandingan performa model
def plot_model_comparison(svm_report, dt_report):
    metrics = ['precision', 'recall', 'f1-score', 'support']
    svm_metrics = [svm_report['macro avg'][metric] for metric in metrics]
    dt_metrics = [dt_report['macro avg'][metric] for metric in metrics]
    
    fig, ax = plt.subplots()
    index = range(len(metrics))
    bar_width = 0.35
    
    bar1 = plt.bar(index, svm_metrics, bar_width, label='SVM')
    bar2 = plt.bar([i + bar_width for i in index], dt_metrics, bar_width, label='Decision Tree')
    
    plt.xlabel('Metrics')
    plt.ylabel('Scores')
    plt.title('Model Comparison')
    plt.xticks([i + bar_width / 2 for i in index], metrics)
    plt.legend()
    st.pyplot(fig)

# Fungsi untuk melakukan K-Fold Cross-Validation
def perform_cross_validation(model, X, y):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    return scores

# Fungsi untuk menampilkan ROC Curve
def plot_roc_curve(model, X_test, y_test, model_name):
    try:
        # Check if model supports predict_proba
        if hasattr(model, "predict_proba"):
            y_score = model.predict_proba(X_test)[:, 1]
        else:
            # Use decision function for SVC if predict_proba is not available
            y_score = model.decision_function(X_test)

        # Tentukan pos_label sesuai dengan kelas target Anda
        pos_label = 'Laris'  # Sesuaikan dengan label yang Anda tentukan sebagai positif

        fpr, tpr, _ = roc_curve(y_test, y_score, pos_label=pos_label)
        roc_auc = auc(fpr, tpr)
        
        fig, ax = plt.subplots()
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve - {model_name}')
        plt.legend(loc="lower right")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error plotting ROC curve: {e}")

# Fungsi untuk membangun halaman training model dan menyimpan model ke dalam history_model
def show_halaman_trainingmodel():
    st.title("Training Model")
    
    # Widget untuk unggah file CSV
    uploaded_file = st.file_uploader("Unggah file CSV", type=['csv'])
    
    if uploaded_file is not None:
        # Baca file CSV
        df = pd.read_csv(uploaded_file)
        
        # Memilih kolom yang diperlukan
        features = ['Jumlah_Penjualan', 'Harga_Awal', 'Total Diskon', 'Rating','Total Harga Produk']
        target = 'Status'
        
        if target not in df.columns:
            st.error(f"Kolom target '{target}' tidak ditemukan dalam dataset.")
            return
        
        # Memisahkan fitur dan target
        X = df[features]
        y = df[target]
        
        # Tombol untuk memicu training model
        if st.button("Train Model"):
            try:
                # Memisahkan data menjadi training dan testing set
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                # Training model SVM
                svm_model = SVC(kernel='linear', probability=True)
                svm_model.fit(X_train, y_train)
                
                # Training model Decision Tree
                dt_model = DecisionTreeClassifier(random_state=42)
                dt_model.fit(X_train, y_train)
                
                # Evaluasi model SVM dengan confusion matrix
                svm_pred = svm_model.predict(X_test)
                svm_cm = confusion_matrix(y_test, svm_pred)
                svm_report = classification_report(y_test, svm_pred, output_dict=True)
                
                # Evaluasi model Decision Tree dengan confusion matrix
                dt_pred = dt_model.predict(X_test)
                dt_cm = confusion_matrix(y_test, dt_pred)
                dt_report = classification_report(y_test, dt_pred, output_dict=True)
                
                # Tampilkan hasil evaluasi
                st.subheader("Evaluasi Model SVM")
                st.write("Confusion Matrix:")
                plot_confusion_matrix(svm_cm, "Confusion Matrix - SVM")
                st.write("Classification Report:")
                st.write(classification_report(y_test, svm_pred))
                
                st.subheader("Evaluasi Model Decision Tree")
                st.write("Confusion Matrix:")
                plot_confusion_matrix(dt_cm, "Confusion Matrix - Decision Tree")
                st.write("Classification Report:")
                st.write(classification_report(y_test, dt_pred))

                # Tampilkan ROC Curve untuk model SVM
                st.subheader("ROC Curve - SVM")
                plot_roc_curve(svm_model, X_test, y_test, "SVM")

                # Tampilkan ROC Curve untuk model Decision Tree
                st.subheader("ROC Curve - Decision Tree")
                plot_roc_curve(dt_model, X_test, y_test, "Decision Tree")
                
                # Tampilkan perbandingan performa model
                st.subheader("Perbandingan Performa Model")
                plot_model_comparison(svm_report, dt_report)
                
                # Simpan model SVM dan Decision Tree ke dalam history_model
                conn = mysql.connector.connect(
                    host="sql12.freemysqlhosting.net",
                    user="sql12721204",
                    password="t4itLMeUj2",
                    database="sql12721204" 
                )
                
                save_model_to_history(svm_model, 'svm_model', conn)
                save_model_to_history(dt_model, 'decision_tree_model', conn)
                
                # Prediksi dan tampilkan produk paling diminati menggunakan model SVM
                predict_and_show_top_products(svm_model, X, df[['Nama_Produk']])
                
            except Exception as e:
                st.error(f"Error during model training: {e}")

# Panggil fungsi untuk menampilkan halaman training model
show_halaman_trainingmodel()
