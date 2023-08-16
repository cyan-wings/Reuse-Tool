import streamlit as st
import pandas as pd
import numpy as np

st.title('Reusability Assessment')

@st.cache_data
def load_data():
    data = pd.read_csv("Data/forWebsite.csv", sep=",", encoding='utf-8')
    return data

data = load_data()

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data.LVUsage, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)