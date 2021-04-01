#!/usr/bin/env python
# coding: utf-8

# In[81]:


#pip install beautifulsoup4


# In[82]:


#pip install geocoder


# In[83]:


#pip install folium


# In[84]:


#pip install geopy


# In[85]:


import numpy as np 
import pandas as pd 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import json
from geopy.geocoders import Nominatim
import requests
from pandas.io.json import json_normalize
import matplotlib.cm as cm
import matplotlib.colors as colors
from sklearn.cluster import KMeans
from bs4 import BeautifulSoup
import folium
import requests 
from pandas.io.json import json_normalize 
from sklearn.cluster import KMeans
from geopy.geocoders import Nominatim 

print('Libraries imported.')


# In[86]:


wiki_original = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text


# In[87]:


wiki_soup = BeautifulSoup(wiki_original, 'xml')


# In[88]:


table_contents=[]
table=wiki_soup.find('table')
for row in table.findAll('td'):
    cell = {}
    if row.span.text=='Not assigned':
        pass
    else:
        cell['PostalCode'] = row.p.text[:3]
        cell['Borough'] = (row.span.text).split('(')[0]
        cell['Neighborhood'] = (((((row.span.text).split('(')[1]).strip(')')).replace(' /',',')).replace(')',' ')).strip(' ')
        table_contents.append(cell)

toronto_data=pd.DataFrame(table_contents)
toronto_data.head()


# In[89]:


toronto_data.shape


# In[90]:


pip install geocoder


# In[91]:


import geocoder # import geocoder

def get_latilong(postal_code):
    lati_long_coords = None
    while(lati_long_coords is None):
        g = geocoder.arcgis('{}, Toronto, Ontario'.format(postal_code))
        lati_long_coords = g.latlng
    return lati_long_coords
    
get_latilong('M4G')


# In[92]:


postal_codes = toronto_data['PostalCode']    
latlong = [ get_latilong(postal_code) for postal_code in postal_codes.tolist() ]


# In[93]:


df_latlong = pd.DataFrame(latlong, columns=['Latitude', 'Longitude'])
toronto_data['Latitude'] = df_latlong['Latitude']
toronto_data['Longitude'] = df_latlong['Longitude']


# In[94]:


toronto_data


# In[95]:


toronto_data1=toronto_data[toronto_data['Borough'].str.contains('Toronto')]
toronto_data2=toronto_data1.reset_index(drop=True)
toronto_data2.head()


# In[96]:


toronto_data2.shape


# In[97]:


#Lat / Long of 43.6532 N and 79.3832


# In[98]:


address = 'Toronto'
geolocator = Nominatim(user_agent="toronto_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(f'The geograpical coordinate of Toronto are {latitude}, {longitude}.')


# In[80]:


map_toronto = folium.Map(location=[latitude, longitude], zoom_start=11)
for lat, lng, borough, neighborhood in zip(toronto_data2['Latitude'], toronto_data2['Longitude'], toronto_data2['Borough'], toronto_data2['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=4,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#87cefa',
        fill_opacity=0.5,
        parse_html=False).add_to(map_toronto)
map_toronto


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




