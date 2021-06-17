#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import sys

def preprocess(page):
    for item in page:
        if 'yyyy' in item.decode('utf-8'):
            new_page = page[page.index(item):-1]
    lis1 = new_page[0].decode('utf-8').split(' ')
    lis1 = [l for l in lis1 if l]
    lis1.append('pro')
    data_lis = []
    for i in range(2,len(new_page)):
        lis = new_page[i].decode('utf-8').split(' ')
        lis= [l for l in lis if l]
        data_lis.append(lis)
    df = pd.DataFrame(columns=lis1,data=data_lis)
    df = df.drop(columns='pro')
    df = df.replace(r'[^0-9.]+','',regex=True)
    #df['sun\r\n'] = df['sun\r\n'].str.replace(r'[^0-9.]+','')
    df['yyyy'] = df['yyyy'].apply(int)
    return df

def weather_analysis(df):
    years_df = df.query('yyyy>2008 & yyyy<2021')
    data = []
    for i in range(1,13):
        row = [i]
        subset_df = years_df[years_df['mm']=='{}'.format(i)]
        subset_df = subset_df.applymap(float)
        row.append(subset_df.tmax.mean())
        row.append(subset_df.tmin.mean())
        row.append(subset_df.rain.mean())
        row.append(subset_df['sun\r\n'].mean())
        data.append(row)
    mean_df = pd.DataFrame(columns=['mm','tmax_mean','tmin_mean','rain_mean','suntime_mean'],data= data)
    one_year_data = years_df.query('yyyy==2020')
    one_year_data = one_year_data.applymap(float)
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    one_year_data.plot(x="mm",y='tmax',ax=ax,title='One Year Maximum Temperature Analysis')
    mean_df.plot(x="mm",y='tmax_mean',ax=ax)
    fig.savefig('maximum temperature.png')
    fig, ax2 = plt.subplots()
    one_year_data.plot(x="mm",y='tmin',ax=ax2,title='One Year Minimum Temperature Analysis')
    mean_df.plot(x="mm",y='tmin_mean',ax=ax2)
    fig.savefig('minimum temperature.png')
    fig, ax3 = plt.subplots()
    one_year_data.plot(x="mm",y='rain',ax=ax3,title='One Year Precipitation Analysis')
    mean_df.plot(x="mm",y='rain_mean',ax=ax3)
    fig.savefig('precipitation.png')
    fig, ax4 = plt.subplots()
    one_year_data.plot(x="mm",y='sun\r\n',ax=ax4,title='One Year Sun Time Analysis')
    mean_df.plot(x="mm",y='suntime_mean',ax=ax4)
    fig.savefig('hours of sunlight.png')

def fetch_data(location):
    url  = 'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/{}data.txt'.format(location)
    header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
          'AppleWebKit/537.11 (KHTML, like Gecko) '
          'Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}

    #the URL where you are requesting at
    req = urllib.request.Request(url=url, headers=header) 
    page = urllib.request.urlopen(req).readlines()
    df = preprocess(page)
    weather_analysis(df)


# In[6]:


fetch_data(sys.argv[1])

