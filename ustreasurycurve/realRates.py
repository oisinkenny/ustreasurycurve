# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 14:24:43 2020

@author: oisin
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

def realRates():
    soup = BeautifulSoup(requests.get('https://data.treasury.gov/feed.svc/DailyTreasuryRealYieldCurveRateData').text,'lxml')
    table = soup.find_all('m:properties')
    tbondvalues = []
    for i in table:
        tbondvalues.append([i.find('d:new_date').text[:10],i.find('d:tc_5year').text,i.find('d:tc_7year').text,i.find('d:tc_10year').text,i.find('d:tc_20year').text,i.find('d:tc_30year').text])
    ustrcurve = pd.DataFrame(tbondvalues,columns=['date','5y','7y','10y','20y','30y'])
    ustrcurve.iloc[:,1:] = ustrcurve.iloc[:,1:].apply(pd.to_numeric)/100
    ustrcurve['date'] = pd.to_datetime(ustrcurve['date'])
    ustrcurve.sort_values('date',inplace=True)
    return ustrcurve
