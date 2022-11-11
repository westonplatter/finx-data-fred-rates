import os

from dotenv import dotenv_values
from fredapi import Fred
import pandas as pd


def get_fred_api_key() -> str:
    """Get the FRED API key from the .env file or OS env var"""
    try:
        config = dotenv_values(".env")
        return config["FRED_API_KEY"]
    except KeyError:
        print("No .env file found. Trying OS environment variables.")
        return os.environ["FRED_API_KEY"]


fred = Fred(api_key=get_fred_api_key())

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
