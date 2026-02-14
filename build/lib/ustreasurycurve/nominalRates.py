# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 14:24:43 2020

@author: oisin
"""


import polars as pl
from datetime import datetime


def nominalRates(date_start=None, date_end=None):
    current_year = datetime.today().strftime('%Y')
    past_year = str(int(current_year) - 1)
    next_year = str(int(current_year) + 1)
    archive_url_base = 'https://home.treasury.gov/system/files/276/yield-curve-rates-1990-'
    current_url_base = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/'
    try:
        archive = pl.read_csv(f'{archive_url_base}{past_year}.csv')
    except:
        archive = pl.read_csv(f'{archive_url_base}{current_year}.csv')
    archive = archive.with_columns(pl.col("Date").str.to_datetime("%m/%d/%y"))
    try:
        current = pl.read_csv(f'{current_url_base}{current_year}/all?type=daily_treasury_yield_curve&field_tdr_date_value={current_year}&page&_format=csv')
    except:
        current = pl.read_csv(f'{current_url_base}{next_year}/all?type=daily_treasury_yield_curve&field_tdr_date_value={next_year}&page&_format=csv')
    current = current.with_columns(pl.col("Date").str.to_datetime("%m/%d/%Y"))
    df = pl.concat([current, archive], how='diagonal')
    df = df.rename(lambda name: name.replace(' Month', 'm').replace(' Yr', 'y').replace(' Mo', 'm').lower())
    df = df.sort('date')
    if date_start is not None:
        df = df.filter(pl.col('date') >= pl.lit(date_start).str.to_date())
    if date_end is not None:
        df = df.filter(pl.col('date') <= pl.lit(date_end).str.to_date())
    return df.to_pandas()


