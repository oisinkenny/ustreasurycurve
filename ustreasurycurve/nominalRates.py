# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 14:24:43 2020

@author: oisin
"""


import polars as pl
from datetime import datetime
import pandas as pd
import re


def nominalRates(date_start=None, date_end=None):

    def sort_period_columns(df):
        def period_to_months(col):
            if col == 'date':
                return -1

            # Extract number and unit using regex
            match = re.match(r'([\d.]+)([my])', col)
            if match:
                value = float(match.group(1))
                unit = match.group(2)
                return value if unit == 'm' else value * 12
            return 0

        sorted_cols = sorted(df.columns, key=period_to_months)
        return df.select(sorted_cols)

    current_year = datetime.today().strftime('%Y')
    csv_archive = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rate-archives'
    z = pd.read_html(csv_archive)
    base_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rate-archives/'
    z = z[3]
    latest_filename = z['Download Archive File'].iloc[-1]
    latest_file_link = fr'{base_url}{latest_filename}'
    archive = pl.read_csv(latest_file_link)
    date_col = None
    for col in archive.columns:
        if col.lower() == "date":
            date_col = col
            break
    if date_col is None:
        raise ValueError("No 'date' column found in the dataframe")
    archive = archive.with_columns(pl.col(date_col).str.to_datetime("%m/%d/%Y"))
    archive = archive.rename({date_col: 'date'})
    archive = archive.with_columns(pl.all().exclude(archive.columns[0]).cast(pl.Float64, strict=False))
    cdfs = []
    for year in [x for x in range(2023, int(current_year) + 1)]:
        cdf = pl.read_csv(
            f'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{year}/all?type=daily_treasury_yield_curve&field_tdr_date_value={year}&page&_format=csv')
        cdfs.append(cdf)
    current = pl.concat(cdfs, how='diagonal')
    date_col = None
    for col in current.columns:
        if col.lower() == "date":
            date_col = col
            break
    if date_col is None:
        raise ValueError("No 'date' column found in the dataframe")
    current = current.with_columns(pl.col(date_col).str.to_datetime("%m/%d/%Y"))
    current = current.rename({date_col: 'date'})
    current = current.with_columns(pl.all().exclude(current.columns[0]).cast(pl.Float64, strict=False))
    current.columns = [col.lower().replace(' month', 'm').replace(' mo', 'm').replace(' yr', 'y') for col in current.columns]
    archive.columns = [col.lower().replace(' month', 'm').replace(' mo', 'm').replace(' yr', 'y') for col in archive.columns]
    df = pl.concat([current, archive], how='diagonal')
    df = df.sort('date')
    df = sort_period_columns(df)
    df = df.to_pandas()
    if date_start is not None:
        df = df.filter(pl.col('date') >= pl.lit(date_start).str.to_date())
    if date_end is not None:
        df = df.filter(pl.col('date') <= pl.lit(date_end).str.to_date())
    df = df.to_pandas()
    df = df.dropna(subset=['10y'])
    return df



