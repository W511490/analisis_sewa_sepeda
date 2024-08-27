import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os

sns.set(style='dark')

def create_byseason(data):
    byseason = data.groupby('season')['cnt'].sum().reset_index()
    byseason.rename(columns={
        'cnt' : 'total_customer'
    }, inplace=True)

    byseason_labels = {1: 'spring', 2: 'summer', 3: 'fall', 4: 'winter'}
    byseason['season'] = byseason['season'].map(byseason_labels)
    return byseason

def create_byholiday(data):
    byholiday = data.groupby('holiday')['registered'].mean().sort_values(ascending=False).reset_index()
    byholiday.rename(columns={
        'registered' : 'registered_customers'
    }, inplace=True)

    byholiday_labels = {0: 'non_holiday', 1: 'holiday'}
    byholiday['holiday'] = byholiday['holiday'].map(byholiday_labels)
    return byholiday

def create_byworkingday(data):
    byworking_day = data.groupby('workingday')['casual'].mean().sort_values(ascending=False).reset_index()
    byworking_day.rename(columns={
        'casual' : 'casual_customers'
    }, inplace=True)

    byworking_day_labels = {0: 'non_workingday', 1: 'workingday'}
    byworking_day['workingday'] = byworking_day['workingday'].map(byworking_day_labels)
    return byworking_day

def create_byseason_weather(data):
    byseason_weather = data.groupby(['season', 'weathersit'])['cnt'].sum().reset_index()
    byseason_weather.rename(columns={
        'cnt' : 'total_customer'
    }, inplace=True)

    byseason_weather_labels1 = {1: 'spring', 2: 'summer', 3: 'fall', 4: 'winter'}
    byseason_weather['season'] = byseason_weather['season'].map(byseason_weather_labels1)

    byseason_weather_labels2 = {1: 'clear weather or partly sunny weather', 
                          2: 'foggy or cloudy weather', 
                          3: 'rainy or snowy weather'}
    byseason_weather['weathersit'] = byseason_weather['weathersit'].map(byseason_weather_labels2)
    return byseason_weather

def create_bike_2011(data):
    bike_2011 = data[data['yr'] == 0]
    bike_2011_df = bike_2011.groupby('mnth')['cnt'].sum().reset_index()
    bike_2011_df.rename(columns={
        'cnt' : 'total_customer'
    }, inplace=True)

    bike_2011_df['mnth'] = pd.to_datetime(bike_2011_df['mnth'], format='%m')
    bike_2011_df['mnth'] = bike_2011_df['mnth'].dt.strftime('%B')
    return bike_2011_df

# bike_data = pd.read_csv('../dashboard/bike.csv')

script_dir = os.path.dirname(os.path.realpath(__file__))

data_file_path = os.path.join(script_dir, '../dashboard/bike.csv')

bike_data = pd.read_csv(data_file_path, encoding='latin1')

byseason_data = create_byseason(bike_data)
byholiday_data = create_byholiday(bike_data)
byworking_day_data = create_byworkingday(bike_data)
byseason_weather_data = create_byseason_weather(bike_data)
bike_2011_data = create_bike_2011(bike_data)

colors = ['#008B8B', '#D3D3D3', '#D3D3D3', '#D3D3D3']

st.header('Rent Bike Dashboard')

# customer sewa sepeda tiap musim
st.subheader('Customers rent bike every season')

total_customer = byseason_data.total_customer.sum()
st.metric('Total Customer: ', total_customer)

st.table(byseason_data[['season', 'total_customer']])

fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(byseason_data['season'], byseason_data['total_customer'], marker='o')
plt.gca().set_yticks([])
ax.set_ylim(0, max(byseason_data['total_customer']) + 100000)
st.pyplot(fig)

# customer terdaftar sewa sepeda pada hari libur dan customer biasa sewa sepeda pada hari kerja
st.subheader('performance of registered customers based on holidays and casual customers based on weekdays.')
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.bar(byholiday_data['holiday'], byholiday_data['registered_customers'], color=colors)
    ax.set_title('AVG registered customers based on holiday', loc='center', fontsize=20)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.bar(byworking_day_data['workingday'], byworking_day_data['casual_customers'], color=colors)
    ax.set_title('AVG casual customers based on holiday', loc='center', fontsize=20)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    st.pyplot(fig)

# musim dan cuaca terhadap pelanggan sewa sepeda
st.subheader('Impact of weather in each season on the total number of bike rent customers')
fig, ax = plt.subplots(figsize=(17, 10))
for weather in byseason_weather_data['weathersit'].unique():
    subset = byseason_weather_data[byseason_weather_data['weathersit'] == weather]
    ax.plot(subset['season'], subset['total_customer'], marker='o', label=f'{weather}')

    for i in range(len(subset)):
        ax.text(subset['season'].iloc[i], subset['total_customer'].iloc[i],
        str(subset['total_customer'].iloc[i]), fontsize=14,
        ha='center', va='bottom')

ax.legend()
ax.grid()
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# performa pelanggan sewa sepeda pada tahun 2011
st.subheader('performance of bike rent customers in 2011')
fig, ax = plt.subplots(figsize=(20, 10))
plt.plot(bike_2011_data['mnth'], bike_2011_data['total_customer'], marker='o')
# for x, y in zip(bike_2011_data['mnth'], bike_2011_data['total_customer']):
#     ax.text(x=x, y=y, s=f'{y}', ha='center', va='bottom', fontsize=12, color='black')
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

st.caption('Copyright (c) Wahyu S 2024')