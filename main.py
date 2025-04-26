import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Nutrisi", layout="centered")

# Header
st.markdown("""
    <h1 style='text-align: center; color: green;'>🍴 Dashboard Nutrisi Makanan & Minuman Indonesia</h1>
    <h5 style='text-align: center; color: grey;'>👨‍💻 oleh Muhammad Rofiif Taqiyyuddin Nabiil | 🆔 2309116029 | 🎓 SI A</h5>
    <hr>
""", unsafe_allow_html=True)

# Sidebar - Filter Nutrisi
st.sidebar.header("⚙️ Filter & Opsi")
selected_nutrient = st.sidebar.selectbox("📌 Pilih Nutrisi untuk Distribusi", ['calories', 'proteins', 'fat', 'carbohydrate'])

# Ambil data dari GitHub
data_url = "https://raw.githubusercontent.com/MuhammadRofif/data/refs/heads/main/streamlit.csv"
try:
    df = pd.read_csv(data_url)
    st.sidebar.success("✅ Data berhasil dimuat")
except Exception as e:
    st.sidebar.error(f"❌ Data gagal dimuat: {e}")
    st.stop()

# Tampilkan Data (Optional Viewer)
with st.expander("📄 Klik untuk melihat 5 data pertama"):
    st.dataframe(df.head())

# 1. Distribusi Nutrisi
st.subheader(f"📊 Distribusi: {selected_nutrient.capitalize()} 🧮")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.histplot(df[selected_nutrient], kde=True, bins=30, color='skyblue', ax=ax1)
ax1.set_title(f'Distribusi {selected_nutrient.capitalize()}', fontsize=14)
st.pyplot(fig1)

# 2. Komposisi Rata-rata Nutrisi
st.subheader("🥗 Komposisi Rata-rata Nutrisi 🍚")
avg_nutrients = df[['calories', 'proteins', 'fat', 'carbohydrate']].mean()
fig2, ax2 = plt.subplots(figsize=(6, 6))
ax2.pie(avg_nutrients, labels=avg_nutrients.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
ax2.set_title("Komposisi Rata-rata Nutrisi", fontsize=10)
st.pyplot(fig2)

# 3. Korelasi antar Nutrisi
st.subheader("🧠 Korelasi antar Nutrisi 🔍")
correlation_matrix = df[['calories', 'proteins', 'fat', 'carbohydrate']].corr()
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax3)
ax3.set_title("Heatmap Korelasi Nutrisi")
st.pyplot(fig3)

# 4. Perbandingan Nutrisi Kalori Tertinggi vs Terendah
st.subheader("⚖️ Perbandingan Nutrisi Kalori Tertinggi 🔺 vs Terendah 🔻")
top10 = df.nlargest(10, 'calories')
bottom10 = df.nsmallest(10, 'calories')
comparison_df = pd.DataFrame({
    "Tertinggi Kalori 🔺": top10[['calories', 'proteins', 'fat', 'carbohydrate']].mean(),
    "Terendah Kalori 🔻": bottom10[['calories', 'proteins', 'fat', 'carbohydrate']].mean()
})
fig4, ax4 = plt.subplots(figsize=(10, 5))
comparison_df.plot(kind='bar', ax=ax4, color=['red', 'blue'])
ax4.set_title("Rata-rata Nutrisi Kalori Tertinggi vs Terendah")
ax4.set_ylabel("Jumlah Nutrisi")
ax4.set_xticklabels(comparison_df.index, rotation=0)
ax4.grid(axis='y')
st.pyplot(fig4)

# 5. Distribusi Kategori Nutrisi
if 'kategori_nutrisi' in df.columns:
    st.subheader("📁 Distribusi Kategori Nutrisi 🗂️")
    kategori_counts = df['kategori_nutrisi'].value_counts()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("📝 Jumlah per Kategori:")
        st.dataframe(kategori_counts.rename("Jumlah"))

    with col2:
        fig5, ax5 = plt.subplots(figsize=(6, 6))
        ax5.pie(kategori_counts, labels=kategori_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        ax5.set_title("Distribusi Kategori Nutrisi")
        st.pyplot(fig5)
else:
    st.warning("⚠️ Kolom 'kategori_nutrisi' tidak ditemukan pada data.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 12px;'>© 2025 - Muhammad Rofiif Taqiyyuddin Nabiil | Sistem Informasi A 📘</p>", unsafe_allow_html=True)
