"""
This script loads Google and Apple Mobility reports, builds cleaned reports in different formats and builds merged files from both sources.

Original data:
    - Google Community Mobility reports: https://www.google.com/covid19/mobility/
    - Apple Mobility Trends reports: https://www.apple.com/covid19/mobility

"""

import io
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


def download_google_reports(directory="google_reports"):
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
        source="Global_Mobility_Report.csv",
        destination="mobility_report.csv",
        report_type="regions"):
    '''Build cleaned Google report for worldwide or for some country (currently only for the US)

        Args:
            source: location of the raw Google CSV report
            destination: destination file path
            report_type: two options available: "regions" - report for worldwide, "US" - report for the US
    '''
    df = pd.read_csv(source, low_memory=False)
    df = df.drop(columns=['country_region_code'])
    df = df.rename(
        columns={
            'country_region': 'country',
            'retail_and_recreation_percent_change_from_baseline': 'retail',
            'grocery_and_pharmacy_percent_change_from_baseline': 'grocery and pharmacy',
            'parks_percent_change_from_baseline': 'parks',
            'transit_stations_percent_change_from_baseline': 'transit stations',
            'workplaces_percent_change_from_baseline': 'workplaces',
            'residential_percent_change_from_baseline': 'residential'})
    if report_type == "regions":
        df = df[df['sub_region_2'].isnull()]
        df = df.drop(columns=['sub_region_2'])
        df = df.rename(columns={'sub_region_1': 'region'})
        df['region'].fillna('Total', inplace=True)
    elif report_type == "US":
        df = df[(df['country'] == "United States")]
        df = df.drop(columns=['country'])
        df = df.rename(
            columns={
                'sub_region_1': 'state',
                'sub_region_2': 'county'})
        df['state'].fillna('Total', inplace=True)
        df['county'].fillna('Total', inplace=True)
    df.to_csv(destination, index=False)


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
        destination=os.path.join(
            'apple_reports',
        "apple_mobility_report.csv"),
        report_type="regions"):
    '''Build cleaned Apple report (transform dates from columns to rows, add country names for subregions and cities)
       for worldwide or for some country (currently only for the US)

        Args:
            source: location of the raw Apple CSV report
            destination: destination file path
            report_type: two options available: "regions" - report for worldwide, "US" - report for the US
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
        apple = apple[['country', 'sub-region', 'subregion_and_city',
                       'geo_type', 'date', 'driving', 'transit', 'walking']]
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

        apple = apple[['state', 'county_and_city', 'geo_type',
                       'date', 'driving', 'transit', 'walking']]
        apple = apple.sort_values(
            by=['state', 'county_and_city', 'geo_type', 'date']).reset_index(drop=True)
    apple.to_csv(destination, index=False)


def build_summary_report(
    apple_source=os.path.join(
        'apple_reports',
        "applemobilitytrends.csv"),
        google_source=os.path.join(
            "google_reports",
            "Global_Mobility_Report.csv"),
    destination=os.path.join(
        "summary_reports",
        "summary_report.csv")):
    '''Build a merged report from Google and Apple data

        Args:
            apple_source: location of the raw Apple CSV report
            google_source: location of the raw Google CSV report
            destination: destination file path
    '''
    # preprocess apple data
    apple = pd.read_csv(apple_source)
    apple['country'] = apple.apply(
        lambda x: x['region'] if x['geo_type'] == 'country/region' else x['country'],
        axis=1)
    apple['sub_region_1'] = apple.apply(
        lambda x: 'Total' if x['geo_type'] == 'country/region' else (
            x['region'] if x['geo_type'] == 'city' or x['geo_type'] == 'sub-region' else (
                x['sub-region'] if x['geo_type'] == 'county' else None)), axis=1)
    apple['sub_region_2'] = apple.apply(
        lambda x: x['region'] if x['geo_type'] == 'county' else 'Total', axis=1)
    apple = apple.drop(
        columns=[
            'alternative_name',
            'geo_type',
            'region',
            'sub-region'])
    apple = apple.melt(
        id_vars=[
            'country',
            'sub_region_1',
            'sub_region_2',
            'transportation_type'],
        var_name='date')
    apple['value'] = apple['value'] - 100
    apple = apple.pivot_table(
        index=[
            'country',
            'sub_region_1',
            'sub_region_2',
            'date'],
        columns='transportation_type').reset_index()
    apple.columns = [t + (v if v != "value" else "")for v, t in apple.columns]

    # convert Apple countries and subregions to Google names
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

    apple['country'] = apple.apply(lambda x: country_AtoG.loc[x['country'], 'country_google'] if (
        country_AtoG is not None and x['country'] in country_AtoG.index) else x['country'], axis=1)
    apple['sub_region_1'] = apple.apply(lambda x: subregions_AtoG.loc[x['sub_region_1'], 'subregion_Google'] if (
        subregions_AtoG is not None and x['sub_region_1'] in subregions_AtoG.index) else x['sub_region_1'], axis=1)

    # process google data
    google = pd.read_csv(google_source, low_memory=False)
    google['sub_region_1'].fillna('Total', inplace=True)
    google['sub_region_2'].fillna('Total', inplace=True)
    google = google.rename(
        columns={
            'country_region': 'country',
            'retail_and_recreation_percent_change_from_baseline': 'retail',
            'grocery_and_pharmacy_percent_change_from_baseline': 'grocery and pharmacy',
            'parks_percent_change_from_baseline': 'parks',
            'transit_stations_percent_change_from_baseline': 'transit stations',
            'workplaces_percent_change_from_baseline': 'workplaces',
            'residential_percent_change_from_baseline': 'residential'})
    summary = pd.merge(
        google, apple, how='outer', left_on=[
            'country', 'sub_region_1', 'sub_region_2', 'date'], right_on=[
            'country', 'sub_region_1', 'sub_region_2', 'date'], sort=True)
    summary = summary.drop(
        columns=['country_region_code'])
    summary['sub_region_2'].fillna('Total', inplace=True)
    summary = summary.sort_values(
        by=['country', 'sub_region_1', 'sub_region_2', 'date'])
    summary.to_csv(destination, index=False)


def slice_summary_report(
    source=os.path.join(
        "summary_reports",
        "summary_report.csv"),
        destination_regions=os.path.join(
            "summary_reports",
            "summary_report_regions.csv"),
    destination_countries=os.path.join(
        "summary_reports",
        "summary_report_countries.csv"),
    destination_US=os.path.join(
        "summary_reports",
        "summary_report_US.csv")):
    '''Slice a merged report into 3 next subreports:
        1) Summary report by regions without US counties
        2) Summary report by countries
        3) Summary report for the US only

        Args:
            source: location of the summary CSV report
            destination_regions: destination for report #1
            destination_countries: destination for report #2
            destination_US: destination for report #3
    '''
    # read full summary report
    summary = pd.read_csv(source, low_memory=False)
    # create report #1
    regions = summary[summary['sub_region_2'] == 'Total']
    regions = regions.drop(columns=['sub_region_2'])
    regions.to_csv(destination_regions, index=False)
    # create report #2
    countries = summary[summary['sub_region_1'] == 'Total']
    countries = countries.drop(columns=['sub_region_1', 'sub_region_2'])
    countries.to_csv(destination_countries, index=False)
    # create report #3
    US = summary[summary['country'] == 'United States']
    US.to_csv(destination_US, index=False)


def csv_to_excel(csv_path, excel_path):
    """Helper function which create Excel file from CSV"""
    df = pd.read_csv(csv_path, low_memory=False)
    df.to_excel(excel_path, index=False, sheet_name='Data')


def run():
    """Run parse flow and build reports"""
    # process Google reports
    new_files_status_google = download_google_reports()
    if new_files_status_google:
        build_google_report(
            source=os.path.join(
                "google_reports",
                "Global_Mobility_Report.csv"),
            destination=os.path.join(
                "google_reports",
                "mobility_report_countries.csv"),
            report_type="regions")
        build_google_report(
            source=os.path.join(
                "google_reports",
                "Global_Mobility_Report.csv"),
            destination=os.path.join(
                "google_reports",
                "mobility_report_US.csv"),
            report_type="US")
        csv_to_excel(
            os.path.join(
                "google_reports",
                "mobility_report_countries.csv"),
            os.path.join(
                "google_reports",
                "mobility_report_countries.xlsx"))
        csv_to_excel(os.path.join("google_reports", "mobility_report_US.csv"),
                     os.path.join("google_reports", "mobility_report_US.xlsx"))
    # process Apple reports
    new_files_status_apple = download_apple_report()
    if new_files_status_apple:
        # build report for the worldwide
        build_apple_report()
        build_apple_report(
            destination=os.path.join(
                'apple_reports',
                "apple_mobility_report_US.csv"),
            report_type="US")
        csv_to_excel(
            os.path.join(
                'apple_reports',
                "apple_mobility_report.csv"),
            os.path.join(
                'apple_reports',
                "apple_mobility_report.xlsx"))
        csv_to_excel(
            os.path.join(
                'apple_reports',
                "apple_mobility_report_US.csv"),
            os.path.join(
                'apple_reports',
                "apple_mobility_report_US.xlsx"))
    # build summary report
    if new_files_status_apple or new_files_status_google:
        print("Merging reports...")
        build_summary_report()
        csv_to_excel(
            os.path.join(
                "summary_reports",
                "summary_report.csv"),
            os.path.join(
                "summary_reports",
                "summary_report.xlsx"))
        # slice summary report
        slice_summary_report()
        csv_to_excel(
            os.path.join(
                "summary_reports",
                "summary_report_regions.csv"),
            os.path.join(
                "summary_reports",
                "summary_report_regions.xlsx"))
        csv_to_excel(
            os.path.join(
                "summary_reports",
                "summary_report_countries.csv"),
            os.path.join(
                "summary_reports",
                "summary_report_countries.xlsx"))
        csv_to_excel(
            os.path.join(
                "summary_reports",
                "summary_report_US.csv"),
            os.path.join(
                "summary_reports",
                "summary_report_US.xlsx"))


if __name__ == '__main__':
    run()
