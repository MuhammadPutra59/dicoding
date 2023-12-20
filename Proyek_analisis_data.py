# -*- coding: utf-8 -*-
"""Copy of Proyek Analisis Data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S9e-UEOo6NugIQs9J6QOCpVvpDp3XaPC

# Proyek Analisis Data: [Input Nama Dataset]
- **Nama:** Muhammad Putra Yubiksana
- **Email:** putrayubik@gmail.com
- **ID Dicoding:** mputray59

## Menentukan Pertanyaan Bisnis

- Pertanyaan 1 : Bagaimana peningkatan total jumlah peminjaman selama 2 tahun terakhir?
- Pertanyaan 2 : Pada musim apa peminjaman paling banyak dilakukan?
- Pertanyaan 3 : Pada cuaca apa peminjaman paling banyak dilakukan?
- Pertanyaan 4 : Pada jam berapa peminjaman paling sering dilakukan pada 1 hari?

## Import Semua Packages/Library yang Digunakan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import plotly.express as px
import datetime
import calendar

"""## Data Wrangling

### Gathering Data
"""

hour_df = pd.read_csv('hour.csv')
hour_df.info()

"""### Assessing Data"""

hour_df.isna().sum()
print("Jumlah duplikasi: ", hour_df.duplicated().sum())

hour_df.describe()

"""### Cleaning Data"""

datetime_columns = ["dteday"]

for column in datetime_columns:
  hour_df[column] = pd.to_datetime(hour_df[column])

hour_df.info()

hour_df['weekday'] = hour_df['dteday'].dt.day_name()
hour_df.head()

hour_df['mnth'] = hour_df['dteday'].dt.month_name()
hour_df.head()

hour_df['yr'] = hour_df['dteday'].dt.year
hour_df.head()

def find_season(season):
    season_string = {1:'Springer', 2:'Summer', 3:'Fall', 4:'Winter'}
    return season_string.get(season)

season_list = []

for season in hour_df['season']:
    season = find_season(season)
    season_list.append(season)

hour_df['season'] = season_list
hour_df.head()

def find_weather(weathersit):
    weather_string = {1:'Clear', 2:'Mist', 3:'Light rain', 4:'Heavy rain'}
    return weather_string.get(weathersit)

weather_list = []

for weathersit in hour_df['weathersit']:
    weathersit = find_weather(weathersit)
    weather_list.append(weathersit)

hour_df['weathersit'] = weather_list
hour_df.head()

hour_df['temp'] = hour_df['temp']*41
hour_df['atemp'] = hour_df['atemp']*50
hour_df['hum'] = hour_df['hum']*100
hour_df['windspeed'] = hour_df['windspeed']*67
hour_df.head()

hour_df.to_csv("cleaned_hour.csv", index=False)

"""## Exploratory Data Analysis (EDA)

### Explore ...
"""

hour_df.describe()

monthly_df = hour_df.resample(rule='M', on='dteday').agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
})
monthly_df = monthly_df.reset_index()
monthly_df = monthly_df.rename(columns={'dteday': 'monthly'})
monthly_df.head()

hourly_df = hour_df.groupby("hr").agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
})


hourly_df = hourly_df.reset_index()
hourly_df.head()

seasonly_df = hour_df.groupby("season").agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
})

seasonly_df = seasonly_df.reset_index()
seasonly_df.head()

weather_df = hour_df.groupby("weathersit").agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
})

weather_df = weather_df.reset_index()
weather_df

hour_df.describe(include="all")

"""## Visualization & Explanatory Analysis

### Pertanyaan 1: Bagaimana peningkatan total jumlah peminjaman selama 2 tahun terakhir?
"""

plt.figure(figsize=(16, 6))
sn.lineplot(x="monthly", y="cnt", data=monthly_df, label='Total')
sn.lineplot(x="monthly", y="casual", data=monthly_df, label='Casual')
sn.lineplot(x="monthly", y="registered", data=monthly_df, label='Registered')

plt.xlabel("Tanggal")
plt.ylabel("Banyak Peminjaman")
plt.title("Jumlah peminjam selama 2 tahun terakhir")

"""### Pertanyaan 2: Pada musim apa peminjaman paling banyak dilakukan?"""

plt.figure()
sn.barplot(x="season",y="cnt",data=hour_df)

plt.xlabel("Musim")
plt.ylabel("Banyak Peminjam")
plt.title("Count of bikeshare rides by Season")
plt.show()

"""### Pertanyaan 3: Pada cuaca apa peminjaman paling banyak dilakukan?"""

plt.figure(figsize=(10,6))
sn.barplot(x='weathersit',y='cnt',data=hour_df)

plt.title('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Jumlah Pengguna Sepeda')
plt.show()

"""### Pertanyaan 4: Pada jam berapa peminjaman paling sering dilakukan pada 1 hari?"""

plt.figure(figsize=(16, 6))

sn.lineplot(x="hr", y="casual", data=hourly_df, label='Casual')
sn.lineplot(x="hr", y="registered", data=hourly_df, label='Registered')

x = np.arange(0, 24, 1)
plt.xticks(x)
plt.xlabel("Jam")
plt.ylabel("Banyak Peminjam")
plt.title("Jam peminjaman")

plt.axvline(x=8, linestyle='--')
plt.axvline(x=17, linestyle='--')
plt.tight_layout()
plt.show()

"""## Conclusion

- Conclution pertanyaan 1:

Pada tahun 2011, peminjaman paling banyak dilakukan pada bulan Juli dan paling rendah pada bulan Januari dan Desember. Pada tahun 2012, Terjadi kenaikan signifikan pada bulan Maret hingga September dimana pada bulan September peminjaman mencapai angka tertinggi. Jumlah peminjaman turun ketika mencapai bulan Desember. Dapat disimpulkan kenaikan jumlah peminjaman terjadi pada tengah tehun dan akan turun pada akhir tahun.
- Conclution pertanyaan 2

Pada dua tahun terakhir peminjaman paling banyak dilakukan pada tengah tahun sampai mendekati akhir tahun. Pada bulan-bulan tersebut teelah memasuki musim panas dan musim gugur. Peminjaman paling banyak dilakukan pada musim gugur, kemudian musim panas pada peringkat ke-2. Musim dingin peminjaman mencapai angka terendah selama setahun dan diatasnya terdapat musim semi.
- Conclution pertanyaan 3

Berdasarkan data peminjaman per-Musim, diketahui bahwa peminjaman paling sering dilakukan pada musim gugur dan musim panas dan cukup jarang pada musim dingin dan musim semi. Hal tersebut dipengaruhi oleh cuaca yang terjadi pada musim-musim tersebut. Peminjaman paling banyak dilakukan pada saat cuaca cerah, cukup jarang melakukan peminjaman pada cuaca berkabut, dan sangat jarang yang meminjam disaat hujan ringan dan berat. Pada bulan April hingga September telah memasuki musim panas dan musim gugur. Cuaca pada kedua musim pada umumnya adalah cerah dan hujan ringan pada musim gugur. Pada musim dingin dan musim semi cuaca yang paling sering terjadi adalah cerah, hujan ringan, hujan berat, dan terkadang disertai kabut. Hal ini memungkinkan terjadinya penurunan pada akhir dan awal tahun dan peningkatan di pertengahan tahun.

- Conclution pertanyaan 4

Pada satu hari, peminjaman paling banyak dilakukan pada pukul 8 pagi (08.00)dan pukul 5 sore (17.00). Hal tersebut dimungkinkan karena pada pagi hari banyak aktivitas yang mengharuskan peminjam untuk pergi keluar rumah seperti bekerja, sekolah, atau aktivitas lainnya. Pada sore hari merupakan waktu para peminjam untuk kembali dari aktivitas sebelumnya dan pulang ke rumah, memungkinkan pelanggan melakukan peminjaman pada jam tersebut. Peningkatan juga terjadi pada pukul 12 siang (12.00), dimungkinkan karena pada saat itu merupakan jam istirahat makan siang. Sedangkan penurunan peminjaman terjadi pada malam hari dan mencapai nilai terendah pada pukul 4 pagi (04.00).
"""