from dotenv import dotenv_values
from fredapi import Fred
import glob
import pandas as pd


config = dotenv_values(".env")
fred = Fred(api_key=config["FRED_API_KEY"])


series_to_get = [
    ("DGS1MO", "1-Month Treasury Constant Maturity Rate"),
    ("DGS3MO", "3-Month Treasury Constant Maturity Rate"),
    ("DGS1", "1-Year Treasury Constant Maturity Rate"),
    ("DGS2", "2-Year Treasury Constant Maturity Rate"),
    ("DGS5", "5-Year Treasury Constant Maturity Rate"),
    ("DGS10", "10-Year Treasury Constant Maturity Rate"),
    ("DGS30", "30-Year Treasury Constant Maturity Rate"),
]

all_dfs = []

for series_id, series_name in series_to_get:
    print(series_name)
    # fetch data
    series = fred.get_series(series_id)
    df = pd.DataFrame(series, columns=['value'])
    # write to file system
    df['name'] = series_id
    df.to_csv(f"{series_id}.csv")
    # append to all list
    all_dfs.append(df)

xdf = pd.concat(all_dfs)
xdf.reset_index(inplace=True)
xdf.rename(columns={'index': 'date'}, inplace=True)
xdf = xdf.pivot(index='date', columns='name', values='value')
xdf.sort_index(inplace=True)
xdf.to_csv("data.csv")

