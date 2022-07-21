# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 14:24:43 2020

@author: oisin
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


def realRates(date_start, date_end):
    year_list = list(range(int(str(date_start)[:4]), int(str(date_end)[:4]) + 1))
    tbondvalues = []
    for year in year_list:
        soup = BeautifulSoup(requests.get('https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml?data=daily_treasury_real_yield_curve&field_tdr_date_value=' + str(year)).text, 'lxml')
        table = soup.find_all('m:properties')
        for i in table:
            try:
                try:
                    thirtyyr = i.find('d:tc_30year').text
                except:
                    thirtyyr = np.NaN
                tbondvalues.append([i.find('d:new_date').text[:10], i.find('d:tc_5year').text, i.find('d:tc_7year').text, i.find('d:tc_10year').text, i.find('d:tc_20year').text, thirtyyr])
            except:
                pass
    ustrcurve = pd.DataFrame(tbondvalues, columns=['date', '5y', '7y', '10y', '20y', '30y'])
    ustrcurve.iloc[:, 1:] = ustrcurve.iloc[:, 1:].apply(pd.to_numeric)/100
    ustrcurve['date'] = pd.to_datetime(ustrcurve['date'])
    ustrcurve.sort_values('date', inplace=True)
    ustrcurve = ustrcurve.loc[(ustrcurve['date'] >= pd.to_datetime(date_start)) & (ustrcurve['date'] <= pd.to_datetime(date_end))].copy()
    ustrcurve.reset_index(drop=True, inplace=True)
    return ustrcurve


