from pathlib import Path
import json
import urllib.request
import requests

import pandas as pd


def check_update(
    tomtom_source,
    api_key_check="JPN_tokyo",
):
    """Check if new TomTom data available

    Args:
        tomtom_source: location of the TomTom report in CSV format (if exist)
        api_key_check: which city will be checked on the TomTom site
    Returns:
        new_files (bool): flag indicating whether or not new data available
    """
    new_files = False
    # check if file available
    if not tomtom_source.is_file():
        new_files = True
    else:
        # get max date from the CSV report
        tomtom = pd.read_csv(tomtom_source, low_memory=False)
        last_report_date = tomtom["date"].max()
        # get last available date from API
        base_api_url = "https://api.midway.tomtom.com/ranking/dailyStats/"
        api_url = base_api_url + api_key_check
        response = requests.get(api_url)
        json_data = response.json()
        last_api_date = json_data[-1]["date"]
        if last_api_date != last_report_date:
            new_files = True

    return new_files


def download_report(alpha_codes_filename):
    """Download TomTom Traffic Index

    Args:
        iso_codes_filename: path to country alpha codes file

    Returns:
        tomtom_data (DataFrame): scraped TomTom report
    """
    # get all available cities
    json_link = (
        "https://www.tomtom.com/en_gb/traffic-index/page-data/ranking/page-data.json"
    )
    with urllib.request.urlopen(json_link) as url:
        json_data = json.loads(url.read().decode())
    # unpack data from json
    json_city_data = json_data["result"]["data"]["allCitiesJson"]["edges"]
    # merge data and select necessary columns
    merged_data = {}
    for k in ["name", "country", "countryName", "continent", "key"]:
        merged_data[k] = tuple(merged_data["node"][k] for merged_data in json_city_data)
    city_data = pd.DataFrame(merged_data)
    # define key exceptions
    key_exceptions = {
        "birmingham-alabama": "birmingham",
        "hamilton-nz": "hamilton",
        "london-ontario": "london",
        "newcastle-au": "newcastle",
        "bengaluru": "bangalore",
    }
    # replace exceptions in DataFrame
    city_data.replace({"key": key_exceptions}, inplace=True)
    # add Alpha3 country codes
    # read file with alpha codes
    alpha_codes = pd.read_csv(alpha_codes_filename)
    # match by alpha2 codes
    city_data = pd.merge(
        city_data, alpha_codes, left_on="country", right_on="Alpha2", how="left"
    )
    city_data.drop("country", axis=1, inplace=True)
    # create api key for scraping data
    city_data["api_key"] = city_data["Alpha3"] + "_" + city_data["key"]
    # scrape data for each city
    base_api_url = "https://api.midway.tomtom.com/ranking/dailyStats/"
    city_df_list = []
    for _, row in city_data.iterrows():
        api_url = base_api_url + row["api_key"]
        response = requests.get(api_url)
        city_df = pd.DataFrame(response.json())
        city_df["country"] = row["countryName"]
        city_df["city"] = row["name"]
        city_df_list.append(city_df)
    # merge all data
    tomtom_data = pd.concat(city_df_list, ignore_index=True)
    tomtom_data = tomtom_data.loc[
        :, ["country", "city", "date", "congestion", "diffRatio"]
    ]
    tomtom_data = tomtom_data.sort_values(by=["country", "city", "date"]).reset_index(
        drop=True
    )
    return tomtom_data


def merge_with_historical_data(tomtom_new, historical_path):
    """Merge new scraped data with historical

    Args:
        tomtom_new (DataFrame): new scraped data
        historical_path: location of the historical TomTom data in CSV format

    Returns:
        DataFrame: merged DataFrame
    """
    tomtom_historical = pd.read_csv(historical_path, low_memory=False)
    tomtom_data = tomtom_historical.append(tomtom_new)
    tomtom_data = tomtom_data.sort_values(by=["country", "city", "date"]).reset_index(
        drop=True
    )

    return tomtom_data