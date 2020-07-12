# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 14:24:43 2020

@author: oisin
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

def nominalRates():
    soup = BeautifulSoup(requests.get('https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData').text,'lxml')
    table = soup.find_all('m:properties')
    tbondvalues = []
    for i in table:
        tbondvalues.append([i.find('d:new_date').text[:10],i.find('d:bc_1month').text,i.find('d:bc_2month').text,i.find('d:bc_3month').text,i.find('d:bc_6month').text,i.find('d:bc_1year').text,i.find('d:bc_2year').text,i.find('d:bc_3year').text,i.find('d:bc_5year').text,i.find('d:bc_10year').text,i.find('d:bc_20year').text,i.find('d:bc_30year').text])
    ustcurve = pd.DataFrame(tbondvalues,columns=['date','1m','2m','3m','6m','1y','2y','3y','5y','10y','20y','30y'])
    ustcurve.iloc[:,1:] = ustcurve.iloc[:,1:].apply(pd.to_numeric)/100
    ustcurve['date'] = pd.to_datetime(ustcurve['date'])
    ustcurve.sort_values('date',inplace=True)
    return ustcurve