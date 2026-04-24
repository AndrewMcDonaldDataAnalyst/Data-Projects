#!/usr/bin/env python
# coding: utf-8

# In[11]:


import json
import os
import ssl
import urllib.parse
import urllib.request
from time import sleep

import certifi
import pandas as pd


FILEPATH = r'C:\Users\admcd\Downloads\Panda Tutorial\api_pull.csv'
API_KEY = "c55af7b04b2b4978a931dd0aab185883"


def api_runner():
    params = urllib.parse.urlencode(
        {
            "start": "1",
            "limit": "15",
            "convert": "USD",
        }
    )
    request = urllib.request.Request(
        f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?{params}",
        headers={
            "Accept": "application/json",
            "X-CMC_PRO_API_KEY": API_KEY,
        },
    )
    context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(request, context=context) as response:
        data = json.load(response)

    df = pd.json_normalize(data['data'])
    df['timestamp'] = pd.to_datetime('now')

    if not os.path.isfile(FILEPATH):
        df.to_csv(FILEPATH, index=False)               # First run: write with header
    else:
        df.to_csv(FILEPATH, mode='a', header=False, index=False)  # Subsequent runs: append


for i in range(333):
    api_runner()
    print(f'API Runner Completed Successfully (run {i + 1}/333)')
    sleep(60)  # sleep for 1 minute


# In[12]:


df72 = pd.read_csv(r'C:\Users\admcd\Downloads\Panda Tutorial\api_pull.csv')
df72


# In[15]:


pd.options.display.float_format = '{:,.2f}'.format


# In[17]:


df72


# In[19]:


df3 = df.groupby('name', sort=False)[['infinite_supply','circulating_supply','total_supply','max_supply']].mean()
df3


# In[21]:


df4 = df3.stack()
df4


# In[23]:


type(df4)


# In[24]:


df5 = df4.to_frame(name='values')
df5


# In[26]:


df5.count()


# In[29]:


index = pd.Index(range(52))

df6 = df5.reset_index()
df6


# In[38]:


df7 = df6.rename(columns={'level_1':'supply'})


# In[42]:


df7['supply']=df7['supply'].replace(['total_supply','infinite_supply','circulating_supply','max_supply'],['total','infinite','circulating','max'])
df7


# In[36]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[43]:


sns.catplot(x='supply', y= 'values', hue='name',data=df7, kind='point')


# In[49]:


df10 = df[['name','quote.USD.price','timestamp']]
df10 = df10.query("name == 'Bitcoin'")
df10


# In[51]:


sns.lineplot(x='timestamp',y='quote.USD.price', data = df10)


# In[ ]:





# In[ ]:




