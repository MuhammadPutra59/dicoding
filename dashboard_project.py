import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import plotly.express as px
import streamlit as st

# load dataset

df = pd.read_csv("https://raw.githubusercontent.com/MuhammadPutra59/dicoding/main/cleaned_hour.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

st.set_page_config(page_title="Bike Sharing Dashboard",
                   layout="wide")

# create helper functions

def create_monthly_df(df):
    monthly_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthly_df.index = monthly_df.index.strftime('%b-%y')
    monthly_df = monthly_df.reset_index()
    monthly_df.rename(columns={
        "dteday": "yearmonth",
        "cnt": "total_user",
        "casual": "casual_user",
        "registered": "registered_user"
    }, inplace=True)
    
    return monthly_df

def create_seasonly_df(df):
    seasonly_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    seasonly_df = seasonly_df.reset_index()
    seasonly_df.rename(columns={
        "cnt": "total_user",
        "casual": "casual_user",
        "registered": "registered_user"
    }, inplace=True)
    
    seasonly_df = pd.melt(seasonly_df,
                                      id_vars=['season'],
                                      value_vars=['total_user'],
                                      var_name='type_of_user',
                                      value_name='count_user')
    
    seasonly_df['season'] = pd.Categorical(seasonly_df['season'],categories=['Springer', 'Summer', 'Fall', 'Winter'])
    
    seasonly_df = seasonly_df.sort_values('season')
    
    return seasonly_df

def create_weather_df(df):
    weather_df = df.groupby("weathersit").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    weather_df = weather_df.reset_index()
    weather_df.rename(columns={
        "cnt": "total_user",
        "casual": "casual_user",
        "registered": "registered_user"
    }, inplace=True)
    
    weather_df = pd.melt(weather_df,
                                      id_vars=['weathersit'],
                                      value_vars=['total_user'],
                                      var_name='type_of_user',
                                      value_name='count_user')
    
    weather_df['weathersit'] = pd.Categorical(weather_df['weathersit'],categories=['Clear', 'Mist', 'Light rain', 'Heavy rain'])
    
    weather_df = weather_df.sort_values('weathersit')
    
    return weather_df

def create_hourly_df(df):
    hourly_df = df.groupby("hr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    hourly_df = hourly_df.reset_index()
    hourly_df.rename(columns={
        "cnt": "total_user",
        "casual": "casual_user",
        "registered": "registered_user"
    }, inplace=True)
    
    return hourly_df

# make filter components (komponen filter)

min_date = df["dteday"].min()
max_date = df["dteday"].max()

# ----- SIDEBAR -----

with st.sidebar:
    # add capital bikeshare logo
    st.image("https://github.com/MuhammadPutra59/dicoding/blob/main/bike-logo.png?raw=true")

    st.sidebar.header("Filter:")

    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Kurun Tanggal", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.sidebar.header("Profile:")

st.sidebar.markdown("Muhammad Putra Yubiksana")

col1, col2 = st.sidebar.columns(2)

with col1:
    st.image("https://github.com/MuhammadPutra59/dicoding/blob/main/GitHub-logo.png?raw=true")
with col2:
    st.markdown("https://github.com/MuhammadPutra59/dicoding")

# hubungkan filter dengan main_df

main_df = df[
    (df["dteday"] >= str(start_date)) &
    (df["dteday"] <= str(end_date))
]

# assign main_df ke helper functions yang telah dibuat sebelumnya

monthly_df = create_monthly_df(main_df)
weather_df = create_weather_df(main_df)
seasonly_users_df = create_seasonly_df(main_df)
hourly_df = create_hourly_df(main_df)

# MAINPAGE
st.title("Bike Sharing Dashboard")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_user = main_df['cnt'].sum()
    st.metric("Total Peminjam", value=total_all_user)
with col2:
    total_casual_user = main_df['casual'].sum()
    st.metric("Total Peminjam Casual", value=total_casual_user)
with col3:
    total_registered_user = main_df['registered'].sum()
    st.metric("Total Peminjam Registered", value=total_registered_user)

st.markdown("---")

# CHART
fig = px.line(monthly_df,
              x='yearmonth',
              y=['casual_user', 'registered_user', 'total_user'],
              color_discrete_sequence=["blue", "green", "orange"],
              markers=True,
              title="Peminjam sepeda selama 2011/2012").update_layout(xaxis_title='', yaxis_title='Total user')

st.plotly_chart(fig, use_container_width=True)

fig1 = px.bar(seasonly_users_df,
              x='season',
              y=['count_user'],
              color='type_of_user',
              color_discrete_sequence=["orange"],
              title='Banyak peminjam berdasarkan musim').update_layout(xaxis_title='season', yaxis_title='Total user')

#st.plotly_chart(fig, use_container_width=True)

fig2 = px.bar(weather_df,
              x='weathersit',
              y=['count_user'],
              color='type_of_user',
              barmode='group',
              color_discrete_sequence=["orange"],
              title='Banyak peminjaman berdasarkn cuaca').update_layout(xaxis_title='Weather', yaxis_title='Total user')

#st.plotly_chart(fig, use_container_width=True)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

fig = px.line(hourly_df,
              x='hr',
              y=['casual_user', 'registered_user'],
              color_discrete_sequence=["blue", "orange"],
              markers=True,
              title='Jam dilakukan peminjaman dalam sehari').update_layout(xaxis_title='', yaxis_title='Total user')

st.plotly_chart(fig, use_container_width=True)

st.caption('Copyright (c), created by Muhammad Putra Y')

# HIDE STREAMLIT STYLE 
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)