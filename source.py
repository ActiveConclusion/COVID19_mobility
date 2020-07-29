"""
This script loads Google, Apple and Waze Mobility reports, builds cleaned reports in different formats and builds merged files from these sources.

Original data:
    - Google Community Mobility reports: https://www.google.com/covid19/mobility/
    - Apple Mobility Trends reports: https://www.apple.com/covid19/mobility
    - Waze COVID-19 local driving trends: https://www.waze.com/covid19

"""

import os
import datetime

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import json

import pandas as pd


def get_google_link():
    '''Get link of Google Community Mobility report file

       Returns:
           link (str): link of Google Community report file
    '''
    # get webpage source
    url = 'https://www.google.com/covid19/mobility/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    csv_tag = soup.find('a', {"class": "icon-link"})
    link = csv_tag['href']
    return link


def download_google_report(directory="google_reports"):
    '''Download Google Community Mobility report in CSV format

        Args:
            directory: directory to which CSV report will be downloaded

        Returns:
            new_files (bool): flag indicating whether or not new files have been downloaded
    '''
    new_files = False

    # create directory if it don't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # download CSV file
    link = get_google_link()
    file_name = "Global_Mobility_Report.csv"
    path = os.path.join(directory, file_name)
    if not os.path.isfile(path):
        new_files = True
        urllib.request.urlretrieve(link, path)
    else:
        path_new = os.path.join(directory, file_name + "_new")
        urllib.request.urlretrieve(link, path_new)
        if os.path.getsize(path) == os.path.getsize(path_new):
            os.remove(path_new)
        else:
            new_files = True
            os.remove(path)
            os.rename(path_new, path)

    if not new_files:
        print('Google: No updates')
    else:
        print('Google: Update available')

    return new_files


def build_google_report(
        source=os.path.join("google_reports", "Global_Mobility_Report.csv"),
        report_type="regions"):
    '''Build cleaned Google report for the worldwide or for some country (currently only for the US)

        Args:
            source: location of the raw Google CSV report
            report_type: two options available: "regions" - report for the worldwide, "US" - report for the US

        Returns:
           google (DataFrame): generated Google report
    '''
    # read the raw report
    google = pd.read_csv(source, low_memory=False)
    # shorten value column names
    google.columns = google.columns.str.replace(
        r'_percent_change_from_baseline', '')
    # remove underscores from column names
    google.columns = google.columns.str.replace(r'_', ' ')
    # rename country column
    google = google.rename(columns={'country region': 'country'})
    if report_type == "regions":
        # note: temp solution
        # remove data of subregions of the second level
        google = google[google['sub region 2'].isnull()]
        # remove metropolitan data
        google = google[google['metro area'].isnull()]
        # rename region column
        google = google.rename(columns={'sub region 1': 'region'})
        google = google.loc[:,
                            ['country',
                             'region',
                             'date',
                             'retail and recreation',
                             'grocery and pharmacy',
                             'parks',
                             'transit stations',
                             'workplaces',
                             'residential']]
        google['region'].fillna('Total', inplace=True)
    elif report_type == "US":
        google = google[(google['country'] == "United States")]
        google = google.rename(
            columns={
                'sub region 1': 'state',
                'sub region 2': 'county'})
        google = google.loc[:,
                            ['state',
                             'county',
                             'date',
                             'retail and recreation',
                             'grocery and pharmacy',
                             'parks',
                             'transit stations',
                             'workplaces',
                             'residential']]
        google['state'].fillna('Total', inplace=True)
        google['county'].fillna('Total', inplace=True)
    return google


def get_apple_link():
    '''Get link of Apple Mobility Trends report file

       Returns:
           link (str): link of Apple Mobility Trends report file
    '''
    # get link via API
    json_link = "https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v3/index.json"
    with urllib.request.urlopen(json_link) as url:
        json_data = json.loads(url.read().decode())
    link = "https://covid19-static.cdn-apple.com" + \
        json_data['basePath'] + json_data['regions']['en-us']['csvPath']
    return link


def download_apple_report(directory="apple_reports"):
    '''Download Apple Mobility Trends report in CSV

        Args:
            directory: directory to which CSV report will be downloaded

        Returns:
            new_files (bool): flag indicating whether or not a new file has been downloaded
    '''
    new_files = False

    if not os.path.exists(directory):
        os.makedirs(directory)

    link = get_apple_link()
    file_name = "applemobilitytrends.csv"
    path = os.path.join(directory, file_name)
    if not os.path.isfile(path):
        new_files = True
        urllib.request.urlretrieve(link, path)
    else:
        path_new = os.path.join(directory, file_name + "_new")
        urllib.request.urlretrieve(link, path_new)
        if os.path.getsize(path) == os.path.getsize(path_new):
            os.remove(path_new)
        else:
            new_files = True
            os.remove(path)
            os.rename(path_new, path)

    if not new_files:
        print('Apple: No updates')
    else:
        print('Apple: Update available')

    return new_files


def build_apple_report(
    source=os.path.join(
        'apple_reports',
        "applemobilitytrends.csv"),
        report_type="regions"):
    '''Build cleaned Apple report (transform dates from columns to rows, add country names for subregions and cities)
       for the worldwide or for some country (currently only for the US)

        Args:
            source: location of the raw Apple CSV report
            destination: destination file path
            report_type: two options available: "regions" - report for the worldwide, "US" - report for the US

        Returns:
           apple (DataFrame): generated Apple report
    '''
    apple = pd.read_csv(source)
    apple = apple.drop(columns=['alternative_name'])
    apple['country'] = apple.apply(
        lambda x: x['region'] if x['geo_type'] == 'country/region' else x['country'],
        axis=1)

    if report_type == 'regions':
        apple = apple[apple.geo_type != 'county']
        apple['sub-region'] = apple.apply(lambda x: 'Total' if x['geo_type'] == 'country/region' else (
            x['region'] if x['geo_type'] == 'sub-region' else x['sub-region']), axis=1)
        apple['subregion_and_city'] = apple.apply(
            lambda x: 'Total' if x['geo_type'] == 'country/region' else x['region'], axis=1)
        apple = apple.drop(columns=['region'])
        apple['sub-region'] = apple['sub-region'].fillna(
            apple['subregion_and_city'])

        apple = apple.melt(
            id_vars=[
                'geo_type',
                'subregion_and_city',
                'sub-region',
                'transportation_type',
                'country'],
            var_name='date')
        apple['value'] = apple['value'] - 100

        apple = apple.pivot_table(
            index=[
                "geo_type",
                "subregion_and_city",
                "sub-region",
                "date",
                "country"],
            columns='transportation_type').reset_index()
        apple.columns = [t + (v if v != "value" else "")
                         for v, t in apple.columns]
        apple = apple.loc[:,
                          ['country',
                           'sub-region',
                           'subregion_and_city',
                           'geo_type',
                           'date',
                           'driving',
                           'transit',
                           'walking']]
        apple = apple.sort_values(by=['country',
                                      'sub-region',
                                      'subregion_and_city',
                                      'date']).reset_index(drop=True)
    elif report_type == "US":
        apple = apple[apple.country == "United States"].drop(columns=[
                                                             'country'])
        apple['sub-region'] = apple['sub-region'].fillna(
            apple['region']).replace({"United States": "Total"})
        apple['region'] = apple.apply(lambda x: x['region'] if (
            x['geo_type'] == 'city' or x['geo_type'] == 'county') else 'Total', axis=1)
        apple = apple.rename(
            columns={
                'sub-region': 'state',
                'region': 'county_and_city'})

        apple = apple.melt(
            id_vars=[
                'geo_type',
                'state',
                'county_and_city',
                'transportation_type'],
            var_name='date')
        apple['value'] = apple['value'] - 100

        apple = apple.pivot_table(
            index=[
                'geo_type',
                'state',
                'county_and_city',
                'date'],
            columns='transportation_type').reset_index()
        apple.columns = [t + (v if v != "value" else "")
                         for v, t in apple.columns]

        apple = apple.loc[:, ['state', 'county_and_city', 'geo_type',
                              'date', 'driving', 'transit', 'walking']]
        apple = apple.sort_values(
            by=['state', 'county_and_city', 'geo_type', 'date']).reset_index(drop=True)
    return apple


def get_waze_links():
    '''Get links of raw Waze local driving Trends report files
    
       Returns:
           link (list): links of Waze local driving Trends report files
    '''
    github_link = "https://raw.githubusercontent.com/ActiveConclusion/waze_mobility_scraper/master/"
    country_level_link = github_link + "Waze_Country-Level_Data.csv"
    city_level_link = github_link + "Waze_City-Level_Data.csv"
    return [country_level_link, city_level_link]


def download_waze_reports(directory="waze_reports"):
    '''Download Waze local driving Trends reports in CSV

        Args:
            directory: directory to which CSV reports will be downloaded

        Returns:
            new_files (bool): flag indicating whether or not a new files has been downloaded
    '''
    new_files = False
    
    # create directory if it don't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    links = get_waze_links()
    file_names = ["Waze_Country-Level_Data.csv", "Waze_City-Level_Data.csv"]
    file_links = dict(zip(file_names, links))
    for file_name in file_names: 
        path = os.path.join(directory, file_name)
        link = file_links[file_name]
        if not os.path.isfile(path):
            new_files = True
            urllib.request.urlretrieve(link, path)
        else:
            path_new = os.path.join(directory, file_name + "_new")
            urllib.request.urlretrieve(link, path_new)
            if os.path.getsize(path) == os.path.getsize(path_new):
                os.remove(path_new)
            else:
                new_files = True
                os.remove(path)
                os.rename(path_new, path)

    if not new_files:
        print('Waze: No updates')
    else:
        print('Waze: Update available')
    
    return new_files


def build_waze_report(countries_source=os.path.join("waze_reports", "Waze_Country-Level_Data.csv"),
                     cities_source=os.path.join("waze_reports", "Waze_City-Level_Data.csv")):
    '''Build cleaned Waze report (transform dates from string to date format, merge country&city-level data,
        add geo_type column)

        Args:
            countries_source: location of the raw Waze country-level CSV report
            cities_source: location of the raw Waze city-level CSV report

        Returns:
           waze (DataFrame): generated Waze report
    '''
    waze_countries = pd.read_csv(countries_source, parse_dates=['Date'])
    waze_cities = pd.read_csv(cities_source, parse_dates=['Date'])
    waze_countries['City'] = 'Total'
    waze_countries['geo_type'] = 'country'
    waze_cities['geo_type'] = 'city'
    
    waze = waze_countries.append(waze_cities)
    waze = waze.rename(columns={'Country':'country', 'City':'city', 
                                'Date':'date', '% Change In Waze Driven Miles/KMs':'driving_waze'})
    waze['driving_waze'] = waze['driving_waze'] * 100
    waze['date'] = waze['date'].dt.date
    waze = waze.loc[:,['country', 'city','geo_type','date', 'driving_waze']]
    waze = waze.sort_values(by=['country', 'city', 'geo_type', 'date']).reset_index(drop=True)
    return waze


def build_summary_report(apple_source, google_source, report_type="regions"):
    '''Build a merged report from Google and Apple data

        Args:
            apple_source: location of the CSV report generated by build_apple_report function
            google_source: location of the CSV report generated by build_google_report function
            report_type: two options available: "regions" - report for the worldwide, "US" - report for the US

        Returns:
            summary (DataFrame): merged report from Google and Apple data
    '''
    apple = pd.read_csv(apple_source, low_memory=False)
    google = pd.read_csv(google_source, low_memory=False)
    summary = pd.DataFrame()
    # build report for regions
    if report_type == "regions":
        apple = apple.rename(columns={'subregion_and_city': 'region'})
        apple = apple.loc[:, ['country', 'region',
                              'date', 'driving', 'transit', 'walking']]
        # get matching table for converting Apple countries and subregions to
        # Google names
        country_AtoG_file = os.path.join(
            'auxiliary_data', 'country_Apple_to_Google.csv')
        subregions_AtoG_file = os.path.join(
            'auxiliary_data', 'subregions_Apple_to_Google.csv')

        if os.path.isfile(country_AtoG_file):
            country_AtoG = pd.read_csv(country_AtoG_file, index_col=0)
        else:
            country_AtoG = None
        if os.path.isfile(subregions_AtoG_file):
            subregions_AtoG = pd.read_csv(subregions_AtoG_file, index_col=0)
        else:
            subregions_AtoG = None
        # convert Apple countries and subregions to Google names
        apple['country'] = apple.apply(lambda x: country_AtoG.loc[x['country'], 'country_google'] if (
            country_AtoG is not None and x['country'] in country_AtoG.index) else x['country'], axis=1)
        apple['region'] = apple.apply(lambda x: subregions_AtoG.loc[x['region'], 'subregion_Google'] if (
            subregions_AtoG is not None and x['region'] in subregions_AtoG.index) else x['region'], axis=1)
        # merge reports
        apple = apple.set_index(['country', 'region', 'date'])
        google = google.set_index(['country', 'region', 'date'])
        summary = google.join(apple, how='outer')
        summary = summary.reset_index(level=['country', 'region', 'date'])
    elif report_type == "US":
        apple = apple.loc[:, ['state', 'county_and_city',
                              'date', 'driving', 'transit', 'walking']]
        apple.loc[apple.state == 'Washington DC',
                  'state'] = 'District of Columbia'
        apple.loc[apple.county_and_city ==
                  'Washington DC', 'county_and_city'] = 'Total'

        google = google.rename(columns={'county': 'county_and_city'})
        # merge reports
        apple = apple.set_index(['state', 'county_and_city', 'date'])
        google = google.set_index(['state', 'county_and_city', 'date'])
        summary = google.join(apple, how='outer')
        summary = summary.reset_index(
            level=['state', 'county_and_city', 'date'])
    return summary


def run():
    """Run parse flow and build reports"""
    # process Google reports
    new_files_status_google = download_google_report()
    if new_files_status_google:
        # build reports
        google_world = build_google_report()
        google_US = build_google_report(report_type="US")
        # write reports to CSV and Excel
        google_world.to_csv(os.path.join("google_reports", "mobility_report_countries.csv"), index=False)
        google_world.to_excel(os.path.join("google_reports", "mobility_report_countries.xlsx"), 
                            index=False, sheet_name='Data', engine = 'xlsxwriter')
        google_US.to_csv(os.path.join("google_reports", "mobility_report_US.csv"), index=False)
        google_US.to_excel(os.path.join("google_reports", "mobility_report_US.xlsx"), 
                            index=False, sheet_name='Data', engine = 'xlsxwriter')
    # process Apple reports
    new_files_status_apple = download_apple_report()
    if new_files_status_apple:
        # build reports
        apple_world = build_apple_report()
        apple_US = build_apple_report(report_type="US")
        # write reports to CSV and Excel
        apple_world.to_csv(os.path.join("apple_reports", "apple_mobility_report.csv"), index=False)
        apple_world.to_excel(os.path.join("apple_reports", "apple_mobility_report.xlsx"), 
                            index=False, sheet_name='Data', engine = 'xlsxwriter')
        apple_US.to_csv(os.path.join("apple_reports", "apple_mobility_report_US.csv"), index=False)
        apple_US.to_excel(os.path.join("apple_reports", "apple_mobility_report_US.xlsx"), 
                        index=False, sheet_name='Data', engine = 'xlsxwriter')
    # process Waze reports
    new_files_status_waze = download_waze_reports()
    if new_files_status_waze:
        # build report
        waze = build_waze_report()
        # write report to CSV and Excel
        waze.to_csv(os.path.join("waze_reports", "waze_mobility.csv"), index=False)
        waze.to_excel(os.path.join("waze_reports", "waze_mobility.xlsx"),
                    index=False, sheet_name='Data', engine='xlsxwriter')
    # build summary reports
    if new_files_status_apple or new_files_status_google:
        print("Merging reports...")
        summary_regions = build_summary_report(os.path.join("apple_reports","apple_mobility_report.csv"),
                                            os.path.join("google_reports", "mobility_report_countries.csv"))
        summary_US = build_summary_report(os.path.join("apple_reports", "apple_mobility_report_US.csv"), 
                                        os.path.join("google_reports", "mobility_report_US.csv"), 'US')
        summary_countries = summary_regions[summary_regions['region']=='Total'].drop(columns=['region'])
        
        print('Writing merged reports to files...')
        summary_regions.to_csv(os.path.join("summary_reports", "summary_report_regions.csv"), index=False)
        summary_regions.to_excel(os.path.join("summary_reports", "summary_report_regions.xlsx"), 
                                index=False, sheet_name='Data', engine = 'xlsxwriter')
        summary_US.to_csv(os.path.join("summary_reports", "summary_report_US.csv"), index=False)
        summary_US.to_excel(os.path.join("summary_reports", "summary_report_US.xlsx"),
                            index=False, sheet_name='Data', engine = 'xlsxwriter')
        summary_countries.to_csv(os.path.join("summary_reports", "summary_report_countries.csv"), index=False)
        summary_countries.to_excel(os.path.join("summary_reports", "summary_report_countries.xlsx"),
                                index=False, sheet_name='Data', engine = 'xlsxwriter')


if __name__ == '__main__':
    run()
