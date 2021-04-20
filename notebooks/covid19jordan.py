#!/usr/bin/env python
# coding: utf-8

# ## What is COVID-19?
# 
# > Coronaviruses are a large family of viruses that may cause respiratory illnesses in humans ranging from common colds to more severe conditions such as Severe Acute Respiratory Syndrome (SARS) and Middle Eastern Respiratory Syndrome (MERS).1
# 'Novel coronavirus' is a new, previously unidentified strain of coronavirus. The novel coronavirus involved in the current outbreak has been named SARS-CoV-2 by the World Health Organization (WHO). 3The disease it causes has been named “coronavirus disease 2019” (or “COVID-19”).`
# 
# ![Coronavirus particle Image](https://www.apta.com/wp-content/uploads/home-banner-1.jpg)

# In[9]:


# Imports
from IPython.core.display import display, HTML 
from IPython.display import YouTubeVideo
import ipywidgets as widget

import folium
from folium import plugins

import numpy as np
import pandas as pd
import json

import plotly as py
import plotly.graph_objects as go
import plotly.express as px


# In[10]:


# load Covid_data
cd=pd.read_csv('https://raw.githubusercontent.com/osamazalaf/project/main/Covidmap.csv')
cd1=pd.read_csv('https://raw.githubusercontent.com/osamazalaf/project/main/Covidmap.csv')

cd2=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')

cd3=pd.read_csv('https://raw.githubusercontent.com/osamazalaf/project/main/Covid.csv')

cd4=pd.read_csv('https://raw.githubusercontent.com/osamazalaf/project/main/Coviddaily.csv')


# In[11]:


cd20=cd2[cd2.Country_Region == 'Jordan']

# total number of confirmed, death and recovered cases
confirmed_total = int(cd20['Confirmed'])
deaths_total = int(cd20['Deaths'])
recovered_total = int(cd20['Recovered'])
active_total = int(cd20['Active'])


# displaying the total stats

display(HTML("<div style = 'background-color: #504e4e; padding: 30px '>" +
             "<span style='color: red; font-size:25px;'> Confirmed: "  + str(confirmed_total) +"</span>" +
             "<span style='color: #fff; font-size:25px;margin-left:20px;'> Deaths: " + str(deaths_total) + "</span>"+
             "<span style='color: lightgreen; font-size:25px; margin-left:20px;'> Recovered: " + str(recovered_total) + "</span>"+
             "<span style='color: lightblue; font-size:25px; margin-left:20px;'> Active: " + str(active_total) + "</span>"+
             "</div>")
       )


# In[29]:


cd1["Confirmed"]=np.log10(cd1["Confirmed"])

# Create map with location start point, zoom level and distance scale
map = folium.Map(location=[32,36], zoom_start=6.45,control_scale=True,height=580,width=750)
                
# load geo_json
country_info = json.load(open('gov.json', encoding='utf-8'))


choropleth = folium.Choropleth(
    geo_data=country_info,
    name='choropleth',
    data=cd1,
    columns=['OBJECTID', 'Confirmed'],
    # see folium.Choropleth? for details on key_on
    key_on='feature.properties.OBJECTID',
    fill_color='YlOrRd',
    fill_opacity=0.5,
    line_opacity=0.5,
    legend_name='Confirmed Cases',
    highlight=True
).add_to(map)

tooltip_text = []
for i in range(0,len(cd)):
    tooltip_text.append('<li><bold> Country: '+str(cd.iloc[i]['City'])+
                          '<li><bold> Confirmed: '+str(cd.iloc[i]['Confirmed']))
tooltip_text
           
# Append a tooltip column with customised text
for i in range(0,len(tooltip_text)):
    country_info['features'][i]['properties']['tooltip1'] = tooltip_text[i]
    
    
choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['tooltip1'], labels=False)
)
        

# add tiles to map
folium.raster_layers.TileLayer('Open Street Map').add_to(map)
folium.raster_layers.TileLayer('CartoDB Positron').add_to(map)


folium.LayerControl().add_to(map)

# add full screen button to map
plugins.Fullscreen(position='topright').add_to(map)

# measure control
measure_control = plugins.MeasureControl(position='topleft', 
                                         active_color='red', 
                                         completed_color='red', 
                                         primary_length_unit='kilometers')

# add measure control to map
map.add_child(measure_control)

# draw tools
# export=True exports the drawn shapes as a geojson file
draw = plugins.Draw(export=False)
# add draw tools to map
draw.add_to(map)


# put in path.html
map.save('map.html')
# display map
map


# In[23]:


fig1 = go.Figure()
fig1.add_trace(go.Scatter(x = cd3['Date'], y = cd3['Confirmed'], mode = 'lines+markers', name = 'Confirmed', line = dict(color = "Red", width = 2)))
fig1.add_trace(go.Scatter(x = cd3['Date'], y = cd3['Recovered'], mode = 'lines+markers', name = 'Recovered', line = dict(color = "Green", width = 2)))
fig1.update_layout(title = 'Jordan Covid-19 Daily Cases', xaxis_tickfont_size = 14, yaxis = dict(title = 'Number of Cases'),height=750)

fig1 = go.FigureWidget(fig1)
fig1


# In[30]:


fig3 = px.pie(cd, values='Confirmed', names='City', color="Confirmed", hole=0.3)
fig3.update_traces(textinfo="label+percent", insidetextfont=dict(color="white"))
fig3.update_layout(legend={"itemclick":False})
fig3.update_layout(title='Cases Percentage of Covid-19 in Jordan',height=580,width=650)

fig3 = go.FigureWidget(fig3)
fig3


# In[24]:


fig5 = px.bar(cd, x='City', y='Confirmed', color='City',
             labels={'pop':'Confirmed Cases'},height=600,width=900)

fig5 = go.FigureWidget(fig5)
fig5


# In[16]:


cd30=cd2[cd2['Active']<100000]

fig4 = go.Figure(data=go.Choropleth(
    locations=cd30['Country_Region'], # Spatial coordinates
    z = cd30['Active'].astype(float), # Data to be color-coded
    locationmode = 'country names', # set of locations match entries in `locations`
    colorscale='YLOrRd'))

fig4.update_layout(
    title_text = 'Active Covid-19 Cases Last Day In Asia <100000',
    geo_scope='asia',height=700,width=850)

fig4.update_geos(fitbounds='locations',visible=False)

fig4=go.FigureWidget(fig4)
fig4


# In[17]:


fig2 = px.scatter(cd4, y="Date", x="Confirmed",
                size="Confirmed", color="City",
                 hover_name="City", log_x=True, size_max=40,title='Jordan Covid19 Daily Cases Compare',height=600,width=1200)

fig2=go.FigureWidget(fig2)
fig2


# In[18]:


id='7e3oAU419k8'
YouTubeVideo(id=id,width=500,height=500)


# ## Notebook covers:
# 
# 1. What is COVID-19?(https://en.wikipedia.org/wiki/Coronavirus_disease_2019)
# 2. Data loading from [Ministry of Health The Hashemite kingdom of Jordan](https://corona.moh.gov.jo/en)
# 
# 
# 
# 
# 
# ## Symptoms:
# People may be sick with the virus for 1 to 14 days before developing symptoms. The most common symptoms of coronavirus disease (COVID-19) are fever, tiredness, and dry cough. Most people (about 80%) recover from the disease without needing special 9treatment.
# * cough
# * fever
# * tiredness
# * difficulty in breathing(severe cases)
# 
# 
# 
# 
# ## More Info on COVID-19:
# * [https://www.worldometers.info/coronavirus/](https://www.worldometers.info/coronavirus/)
# 
# 
# 
# 
# 
# 
# ## If You Want The Site Send You The Latest Information about Covid-19 Virus in Jordan, Please Contact Us By The Following Emai: (coviid19jo@gmail.com)
