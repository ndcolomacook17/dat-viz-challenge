# Import necessary libs 
from datetime import time
import streamlit as st 
import pydeck as pdk
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import math


df = pd.read_csv('hazard_for_challenge.csv')

# Inro section to visualize assets 
st.title('Failure Analysis of Assets in NYC')
st.header('Asset Locations')
intro_text= "Maximizing the uptime of the total assets is the central question we'd like to understand. First let's take a look at the "
st.write("""
    Maximizing the uptime of the total assets is the central question we'd like to understand. From the asset data, it 
    looks like there are {} total assets around the NYC area. Let's first take a look at where these assets are within 
    the city: 
""".format(df.shape[0]))

asset_locations = df[['longitude','latitude']]
st.map(asset_locations)
st.caption('All {} asset locations, zoom in to view asset density in certain Manhattan areas.'.format(df.shape[0]))
st.write("""
    From this we can see that all assets are contained not just within NYC but solely within Manhattan, decreasing the 
    total geographical space needed when searching for faulty assets.
""")

# Analysis of asset failure as a function of time, aka P(failure)(t)
st.header('Average Asset Failure over Time')
st.write("""
    From our asset data, there are {} timestamps recording the hazard, or failure probability, of that asset within the
    next 12 hours. This provides use with failure probability data between Oct. 27th, 2012-Nov. 9th 2012. To understand 
    how failure probability evolves over time, let's analyze the average failure probability over this 2 week period:
""".format(df.drop(['reference','latitude', 'longitude'], axis=1).shape[1]))

# Pandas manipulation to extract correct data for P(failure)(t)
avg_asset_fail = df.drop(['reference', 'longitude', 'latitude'], axis=1).apply(np.mean)
avg_asset_fail_pct = avg_asset_fail * 100

# Plotting in streamlit using matplotlib functionalities 
avg_fig1 = plt.figure()
avg_asset_fail_pct.plot(title='Average Asset Failure Probability (Oct. 27th-Nov. 8th, 2012)', rot=45, marker='+')
plt.xlabel('Timestamps')
plt.ylabel('Average Asset Failure Probability (%)')
st.pyplot(avg_fig1)

st.caption('Failure probability over time for all assets. Notice the sharp spike in hazard rate between Oct. 29th and Nov. 1st.')

st.write("""
    As we approach winter, on average all of the assets have a higher change of failing, which may indicate that as we 
    get into the even colder days of the year (January-March) for NYC, this trend could continue. Although this can't be 
    totally confirmed through the asset data, an analysis of the same time interval in multiple years could shed light 
    on whether there is in fact clear seasonality with respect to temperature fluctuations occuring. Alternatively, 
""")

st.header('Most Hazardous Assets Search')
st.markdown("""
    To find any extremely hazardous assets, we need to first determine how many assets can be repaired/replaced given 
    a budget constraint. Given that we don't have repair cost data, as a baseline we can just assume cost is uniform 
    across assets __(each asset repair cost is $1, this can easily be attenuated if needed)__. Based off of the asset 
    data, we can then determine the most faulty assets within our budget, find their location, and browse through 
    12-hour intervals to examine how the set of faulty assets change: 
""")



asset_slider_val = st.slider('Number of Assets', min_value=0, max_value=df.shape[0])
timestamp_cols = df.drop(['reference', 'longitude', 'latitude'], axis=1).columns
ts_slider_val = st.select_slider('12-hour Time Period', timestamp_cols)


def asset_map(asset_num, timestamp):
    '''Takes in the slider values, returns custom header description, map of desired assets for the timestamp, and 
    table of top hazardous assets'''
    top_asset_hfs = df.sort_values(by=timestamp, ascending=False)
    subhead = st.subheader('Top {} hazardous assets at timestamp: {}'.format(math.floor(float(asset_num)), timestamp))
    viz = st.map(top_asset_hfs[0:math.floor(float(asset_num))][['longitude', 'latitude']])

    if asset_num > 20:
        asset_info = st.table(top_asset_hfs[0:20][['reference','longitude', 'latitude', timestamp]])
        return [subhead, viz, asset_info]

    asset_info = st.table(top_asset_hfs[0:math.floor(float(asset_num))][['reference','longitude', 'latitude', timestamp]])
    return [subhead, viz, asset_info]

#def haz_assets_table(num, ts):

asset_map(asset_slider_val, ts_slider_val)

st.header('Soluton')
st.markdown("""
    After exploring the most hazardous assets over each timestamp, we can notice that the top 20 in this category do not 
    change. This allows us to identify these as the __most hazardous assets overall__. Below we look at the maximum failure
    probability for all {} assets and we can see the clear outliers that match up with the data above: 
""".format(df.shape[0]))

#TODO: Correct data, figure out how to format nicely, explore plot styles 
max_asset_fail = df.drop(['reference', 'longitude', 'latitude'], axis=1).apply(np.max, axis=1)
max_asset_fail_pct = max_asset_fail * 100

fig2 = plt.figure()
max_asset_fail_pct.plot(title='Maximum Failure Probability for each Asset (Oct. 27th-Nov. 8th, 2012)', rot=45)
plt.xlabel('Asset #')
plt.ylabel('Asset Failure Probability (%)')
st.pyplot(fig2)

st.markdown("""
    As a final suggestion from this analysis, __these are the top 20 assets that need to be repaired/replaced first to maximize the 
    uptime of the equipment fleet:__ 
""")

df_max = max_asset_fail_pct.to_frame()

df_max['Asset'] = df.sort_values(by='11/9/12 0:00', ascending=False)['reference']
df_max['Failure Probability (%)'] = df_max[0]

st.table(
    df_max.sort_values(by=0, ascending=False)[0:19][['Asset','Failure Probability (%)']]
    )