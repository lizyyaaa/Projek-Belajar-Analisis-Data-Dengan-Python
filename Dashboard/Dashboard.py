import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur warna latar belakang
sns.set(style='dark')

# Fungsi untuk visualisasi penyewaan berdasarkan musim
def penyewaan_per_musim(data_hari):
    plt.clf()
    data_hari['season_name'] = data_hari['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    penggunaan_per_musim = data_hari.groupby('season_name')['cnt'].mean()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(penggunaan_per_musim, labels=penggunaan_per_musim.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2'))
    ax.set_title('Persentase Rata-rata Penyewaan Sepeda per Musim', fontsize=20)
    ax.axis('equal')
    st.pyplot(fig)

# Fungsi untuk visualisasi penyewaan berdasarkan cuaca
# Fungsi untuk visualisasi penyewaan berdasarkan cuaca
def penyewaan_berdasarkan_cuaca(data_jam):
    plt.clf()
    data_jam['weathersit'] = data_jam['weathersit'].replace({1: 'Clear', 2: 'Mist', 3: 'Light snow', 4: 'Heavy rain'})
    rata_rata_cuaca = data_jam.groupby('weathersit')['cnt'].mean().reset_index()

    # mengurutkan data dari yang tertinggi penyewaannya
    rata_rata_cuaca = rata_rata_cuaca.sort_values(by='cnt', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='cnt', y='weathersit', data=rata_rata_cuaca, hue='weathersit', palette='coolwarm', ax=ax, legend=False)
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontsize=20)
    ax.set_xlabel('Rata-rata Jumlah Penyewaan Sepeda', fontsize=15)
    ax.set_ylabel(None)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.grid(axis='y')
    st.pyplot(fig)

# FFungsi untuk visualisasi penyewaan berdasarkan jam
def penyewaan_per_jam(data_jam):
    plt.clf()
    total_penyewaan = data_jam.groupby('hr')['cnt'].sum().reset_index()

    # Ensure we have data for all hours from 0 to 23
    all_hours = pd.DataFrame({'hr': range(24)})
    total_penyewaan = all_hours.merge(total_penyewaan, on='hr', how='left').fillna(0)

    # Membuat chart
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='hr', y='cnt', data=total_penyewaan, marker='o', color='b')

    # Mengatur judul dan label
    plt.title('Jumlah Penyewaan Sepeda Berdasarkan Jam', fontsize=16)
    plt.xlabel('Jam', fontsize=14)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
    plt.xticks(range(24), fontsize=12)  # Menampilkan label jam
    plt.grid()

    # Menampilkan grafik
    st.pyplot(plt) 

# FFungsi untuk visualisasi penyewaan berdasarkan kategori kelembaban
def penyewaan_kelembaban(data_jam):
    plt.clf()
    bins_kelembaban = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    label_kelembaban = ['Very Dry', 'Dry', 'Normal', 'Humid', 'Very Humid']

    # Categorizing the 'hum' column into groups
    data_jam['humidity_category'] = pd.cut(data_jam['hum'], bins=bins_kelembaban, labels=label_kelembaban)

    # menghitung jumlah penyewaan berdasarkan kelembaban
    penggunaan_kelembaban = data_jam.groupby('humidity_category', observed=True)['cnt'].mean().reset_index()

    # membuat chart
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='humidity_category', y='cnt', data=penggunaan_kelembaban, hue='humidity_category', palette='coolwarm', ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kelembaban', fontsize=20)
    ax.set_xlabel('Kategori Kelembaban', fontsize=15)
    ax.set_ylabel('Rata-rata Jumlah Penyewaan Sepeda', fontsize=15)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.grid(axis='y')
    st.pyplot(fig)

# Load dataset 
data_hari = pd.read_csv("Dashboard/day.csv")
data_jam = pd.read_csv("Dashboard/hour.csv")

# Streamlit Layout
st.title("Dashboard Analisis Penyewaan Sepeda Sistem Capital Bikeshare, Washington D.C., USA")
st.sidebar.header("**Dashboard**")

# Sidebar Elements
st.sidebar.image("https://e7.pngegg.com/pngimages/227/758/png-clipart-bicycle-sharing-system-bike-rental-cycling-bicycle-child-hand.png", 
                 width=100)
st.sidebar.markdown("Analisis penyewaan sepeda tahun 2011-2012")

# Adding selection for visualization types
tipe_visualisasi = st.sidebar.selectbox("Pilih Data Analisis:", ["Penyewaan per Musim", "Penyewaan Berdasarkan Cuaca", "Penyewaan Berdasarkan Jam", "Penyewaan Berdasarkan Kelembaban"])

# Display selected visualization
if tipe_visualisasi == "Penyewaan per Musim":
    penyewaan_per_musim(data_hari)
elif tipe_visualisasi == "Penyewaan Berdasarkan Cuaca":
    penyewaan_berdasarkan_cuaca(data_jam)
elif tipe_visualisasi == "Penyewaan Berdasarkan Jam":
    penyewaan_per_jam(data_jam)
elif tipe_visualisasi == "Penyewaan Berdasarkan Kelembaban":
    penyewaan_kelembaban(data_jam)

# Kesimpulan
st.header("Insight")

# Insight musim
if tipe_visualisasi == "Penyewaan per Musim":
    st.write(""" 
    - Penyewaan Sepeda pada Musim Gugur atau Fall memiliki rata-rata penyewaan tertinggi mencapai 31,4%, sedangkan Spring menunjukkan persentase terendah, yaitu 14,5%
    """)

# Insight cuaca
elif tipe_visualisasi == "Penyewaan Berdasarkan Cuaca":
    st.write(""" 
    - Penyewaan sepeda paling banyak disewa pada kondisi cuaca cerah atau Clear. Penyewaan menurun drastis pada kondisi cuaca yang buruk, seperti Heavy Rain, yang mengindikasikan bahwa cuaca sangat mempengaruhi penyewaan sepeda.
    """)

# Insight jam
elif tipe_visualisasi == "Penyewaan Berdasarkan Jam":
    st.write(""" 
    - Penyewaan dengan jumlah penyewaan tertinggi terjadi sekitar jam 17:00 dan penyewaan terendah terjadi sekitar jam 04.00.
    """)

# Insight kelembaban
elif tipe_visualisasi == "Penyewaan Berdasarkan Kelembaban":
    st.write(""" 
    - Penyewaan sepeda tertinggi terjadi ketika kelembaban pada tingkat Dry dan disusul dengan Very Dry. Sedangkan penyewaan terendah terjadi ketika kelembaban udara pada tingkat Very Humid.
    """)
