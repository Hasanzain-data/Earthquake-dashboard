import streamlit as st
import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).parent / '2.5_week.csv'


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df['time'] = pd.to_datetime(df['time'])
    return df


df = load_data()

st.title('Global Earthquake Dashboard')
st.write('Interactive dashboard analysing USGS Magnitude 2.5+ Earthquakes')
st.subheader('Global Earthquake Analysis')
st.sidebar.header('Filters')
st.sidebar.write('Use the filters below to explore the data.')

mag_min = st.sidebar.slider('Minimum Magnitude', 
    min_value=float(df['mag'].min()), 
    max_value=float(df['mag'].max()), 
    value=float(df['mag'].min()))

depth_max = st.sidebar.slider('Maximum Depth (km)', 
    min_value=float(df['depth'].min()), 
    max_value=float(df['depth'].max()), 
    value=float(df['depth'].max()))

filtered_df = df[(df['mag'] >= mag_min) & (df['depth'] <= depth_max)]

st.header('Magnitude Distribution')
st.write('This chart shows the distribution of earthquake magnitudes.')
mag_bins = (filtered_df['mag'] // 0.5) * 0.5
mag_counts = mag_bins.value_counts().sort_index()
mag_counts.index = [f'{m:.1f}-{m + 0.5:.1f}' for m in mag_counts.index]
st.bar_chart(mag_counts)

st.header('Earthquake Map')
st.write('This map shows the global location of earthquakes.')
map_df = filtered_df[['latitude', 'longitude']].dropna()
map_df.columns = ['lat', 'lon']
st.map(map_df)

st.header('Depth Analysis')
st.write('This chart shows earthquake depth over time.')
depth_df = filtered_df[['time', 'depth']].sort_values('time').set_index('time')
st.line_chart(depth_df)

st.header('Earthquake Data Table')
st.write('Filtered earthquake records.')
st.write(filtered_df[['time', 'place', 'mag', 'depth']].reset_index(drop=True))
st.caption('Data source: USGS Earthquake Hazards Program')