import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

st.set_page_config(layout="wide", page_title="Distribusi & Outlier Analyzer")

menu = st.sidebar.radio("Navigasi Menu", ["🏠 Home", "📘 Penjelasan Teori", "📊 Analisis Distribusi"])

if menu == "🏠 Home":
    st.title("🔍 Aplikasi Analisis Distribusi & Outlier")
    st.write("""
    Aplikasi ini membantu kamu:
    - Memahami teori distribusi dan outlier
    - Mengunggah file data dan mengevaluasi distribusi kolom numerik
    - Mendeteksi outlier dengan metode statistik (IQR)
    - Membandingkan distribusi sebelum dan sesudah pembersihan outlier
    """)

elif menu == "📘 Penjelasan Teori":
    st.title("📘 Penjelasan Teori: Distribusi & Outlier")

    st.header("1. 🎯 Apa itu Distribusi?")
    st.markdown("""
    Distribusi menggambarkan **penyebaran nilai data** dalam suatu variabel. Distribusi membantu kita memahami:
    - Apakah data **terpusat di tengah** atau **menyebar ke ekstrem**
    - Apakah data **simetris** atau **miring ke kiri/kanan (skewed)**
    - Apakah data mengikuti pola **Normal/Gaussian** atau tidak
    """)

    st.header("2. 🔍 Jenis-Jenis Distribusi")
    st.image("distribusi_jenis.png", use_container_width=True)
    st.caption("""
    - 📈 Distribusi Normal (Simetris): Bentuk lonceng, data terpusat di tengah  
    - 📉 Skew Kanan: Ekor panjang di kanan, banyak data kecil  
    - 📉 Skew Kiri: Ekor panjang di kiri, banyak data besar
    """)

    st.header("3. 🧨 Apa itu Outlier?")
    st.markdown("""
    **Outlier** adalah nilai yang:
    - **Jauh berbeda** dari mayoritas data
    - Bisa disebabkan oleh kesalahan input, variasi alami, atau fenomena ekstrem

    > Contoh outlier: penghasilan rata-rata karyawan Rp 10 juta, tapi ada 1 orang dengan Rp 100 juta.
    """)

    st.header("4. 📐 Deteksi Outlier dengan IQR (Interquartile Range)")
    st.markdown("""
    Metode IQR adalah metode statistik untuk mendeteksi outlier menggunakan:
    - **Q1**: Kuartil 25%
    - **Q3**: Kuartil 75%
    - **IQR** = Q3 - Q1

    Batas Outlier:
    - **Bawah** = Q1 – 1.5 × IQR
    - **Atas** = Q3 + 1.5 × IQR

    Semua data di luar rentang tersebut dianggap **outlier**.
    """)

    st.image("outlier.png", use_container_width=True)
    st.caption("Visualisasi Boxplot: nilai di luar whisker adalah outlier")
    st.markdown("""
    Gambar di atas menggabungkan:
    
    1. **Boxplot (atas)**: Menunjukkan median, Q1, Q3, serta batas outlier (Q1 - 1.5×IQR dan Q3 + 1.5×IQR).
    2. **Distribusi Normal (tengah)**: Menjelaskan pembagian area distribusi berdasarkan IQR:
        - Sekitar **50% data** berada di antara Q1 dan Q3
        - Sekitar **24.65% data** di luar Q1 dan Q3 tapi masih dalam distribusi normal
    3. **Distribusi Normal (bawah)**: Menunjukkan bahwa:
        - **68.27% data** berada di ±1σ dari mean
        - **15.87%** berada di masing-masing sisi di luar ±1σ

    Hubungan ini sangat penting untuk:
    - Memahami **penyebaran data** dan seberapa normal distribusinya
    - Mengidentifikasi **potensi outlier** secara visual dan statistik
    """)

    st.header("5. 🧠 Mengapa Outlier Perlu Diperhatikan?")
    st.markdown("""
    - Outlier dapat **mengacaukan rata-rata dan model statistik**
    - Bisa menyebabkan hasil yang **menyesatkan**
    - **Perlu dipertimbangkan**: apakah outlier perlu dihapus, disesuaikan, atau dipertahankan
    """)

    st.header("6. 📊 Visualisasi Umum Distribusi & Outlier")
    st.markdown("""
    | Visualisasi | Fungsi |
    |-------------|--------|
    | **Histogram** | Menampilkan bentuk distribusi |
    | **Boxplot** | Mengidentifikasi outlier |
    | **Skewness/Kurtosis** | Mengukur kemiringan dan ketajaman distribusi |
    """)
    st.header("7. 📘 Ringkasan Tipe Distribusi")

    st.markdown("""
    | Jenis Distribusi     | Skewness       | Bentuk Ekornya         | Hubungan Mean–Median–Mode     |
    |----------------------|----------------|-------------------------|-------------------------------|
    | Simetrik (Normal)    | 0              | Seimbang kiri–kanan     | Mean = Median = Mode          |
    | Skew Kiri (Negatif)  | < 0            | Ekor kiri panjang        | Mean < Median < Mode          |
    | Skew Kanan (Positif) | > 0            | Ekor kanan panjang       | Mean > Median > Mode          |
    """, unsafe_allow_html=True)

    st.header("✅ Tips Praktis")
    st.markdown("""
    | Tujuan | Rekomendasi |
    |--------|-------------|
    | Deteksi outlier | Gunakan boxplot + IQR |
    | Pemeriksaan distribusi | Gunakan histogram + skewness |
    | Pra-pemodelan | Pertimbangkan hapus/transformasi outlier |
    """)

    st.success("Penjelasan teori ini membantu Anda memahami konteks statistik sebelum eksplorasi data lebih lanjut.")

elif menu == "📊 Analisis Distribusi":
    st.title("📊 Analisis Distribusi & Deteksi Outlier")

    uploaded_file = st.file_uploader("📤 Upload file CSV atau Excel", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith("csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")
            st.stop()

        st.subheader("📄 Preview Data")
        st.dataframe(df.head())

        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not num_cols:
            st.warning("Tidak ada kolom numerik ditemukan.")
            st.stop()

        selected_col = st.selectbox("Pilih kolom numerik", num_cols)

        if selected_col:
            original_data = df[selected_col].dropna()
            data = original_data.copy()

            st.subheader("📊 Statistik Deskriptif")
            st.write(data.describe())

            st.subheader("📈 Histogram Distribusi")
            fig1, ax1 = plt.subplots()
            sns.histplot(data, kde=True, ax=ax1)
            st.pyplot(fig1)

            st.subheader("📦 Boxplot untuk Deteksi Outlier")
            fig2, ax2 = plt.subplots()
            sns.boxplot(x=data, ax=ax2)
            st.pyplot(fig2)
        
            st.subheader("🚨 Deteksi Outlier (Metode IQR)")
            factor = st.slider("Tentukan faktor IQR", 0.5, 3.0, 1.5, 0.1)
            q1 = data.quantile(0.25)
            q3 = data.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - factor * iqr
            upper = q3 + factor * iqr
            outliers = data[(data < lower) | (data > upper)]

            st.markdown(f"""
            **Jumlah Outlier:** {len(outliers)}  
            **Batas Bawah:** {lower:.2f}  
            **Batas Atas:** {upper:.2f}
            """)

            st.subheader("📉 Histogram dengan Batas Outlier")
            fig3, ax3 = plt.subplots()
            sns.histplot(data, kde=True, ax=ax3)
            ax3.axvline(lower, color='red', linestyle='--', label='Lower Bound')
            ax3.axvline(upper, color='red', linestyle='--', label='Upper Bound')
            ax3.legend()
            st.pyplot(fig3)

            remove_outlier = st.checkbox("🧹 Hapus outlier dari data")
            if remove_outlier:
                data = data[(data >= lower) & (data <= upper)]
                st.success("Outlier telah dihapus dari data.")

            st.subheader("📊 Perbandingan Statistik Sebelum & Sesudah Outlier Dihapus")
            compare_df = pd.DataFrame({
                "Sebelum Outlier Dihapus": original_data.describe(),
                "Setelah Outlier Dihapus": data.describe()
            })
            st.dataframe(compare_df)

            st.subheader("📈 Histogram Perbandingan")
            fig4, (ax4, ax5) = plt.subplots(1, 2, figsize=(14, 4))
            sns.histplot(original_data, kde=True, ax=ax4, color='orange')
            ax4.set_title("Sebelum")
            sns.histplot(data, kde=True, ax=ax5, color='green')
            ax5.set_title("Sesudah")
            st.pyplot(fig4)

            st.subheader("📦 Boxplot Perbandingan")
            fig5, (bx1, bx2) = plt.subplots(1, 2, figsize=(14, 3))
            sns.boxplot(x=original_data, ax=bx1, color='orange')
            bx1.set_title("Sebelum")
            sns.boxplot(x=data, ax=bx2, color='green')
            bx2.set_title("Sesudah")
            st.pyplot(fig5)

            st.subheader("🧪 Uji Normalitas (Shapiro-Wilk)")
            try:
                stat, p = stats.shapiro(data)
                st.markdown(f"**Statistik = {stat:.4f}**, **p-value = {p:.4f}**")
                if p > 0.05:
                    st.success("Distribusi kemungkinan normal (p > 0.05)")
                else:
                    st.warning("Distribusi kemungkinan tidak normal (p ≤ 0.05)")
            except Exception as e:
                st.error(f"Uji normalitas gagal: {e}")

            if len(outliers) > 0:
                st.subheader("📥 Download Data Outlier")
                csv = outliers.to_csv(index=False).encode('utf-8')
                st.download_button("Download Outlier sebagai CSV", data=csv, file_name="outliers.csv", mime="text/csv")
                st.dataframe(outliers)

            st.subheader("🧠 Insight Otomatis")
            total = len(original_data)
            st.write(f"- Kolom `{selected_col}` memiliki **{len(outliers)} outlier** dari total **{total} data** ({(len(outliers)/total)*100:.2f}%).")
            if p > 0.05:
                st.write("- Distribusi data mendekati **normal**. Cocok untuk analisis parametrik.")
            else:
                st.write("- Distribusi data **tidak normal**. Gunakan metode statistik non-parametrik.")
