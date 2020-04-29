import io
import os
import datetime

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re
import json

import pandas as pd


def download_google_reports(
        directory_pdf=os.path.join(
            "google_reports",
            "pdf_reports"),
        directory_csv="google_reports"):
    """Download all new Google Community Mobility Reports
    """
    url = 'https://www.google.com/covid19/mobility/'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    new_files = False

    if not os.path.exists(directory_pdf):
        os.makedirs(directory_pdf)
    if not os.path.exists(directory_csv):
        os.makedirs(directory_csv)

    # download CSV
    csv_tag = soup.find('a', {"class": "icon-link"})
    link = csv_tag['href']
    file_name = link[link.find('mobility') + len('mobility') + 1:]
    if link[-3:] == "csv":
        path = os.path.join(directory_csv, file_name)
        if not os.path.isfile(path):
            new_files = True
            urllib.request.urlretrieve(link, path)
            print(file_name)
            time.sleep(1)
        else:
            path_new = os.path.join(directory_csv, file_name + "_new")
            urllib.request.urlretrieve(link, path_new)
            if os.path.getsize(path) == os.path.getsize(path_new):
                os.remove(path_new)
            else:
                new_files = True
                os.remove(path)
                os.rename(path_new, path)
    # download PDFs
    json_data = re.search(
        r"window.templateData=JSON.parse\('([^']+)", response.text)
    json_data = bytes(json_data.groups()[0], 'utf-8').decode('unicode_escape')
    json_data = json.loads(json_data)
    for elem in json_data['countries']:
        link = elem['pdfLink']
        file_name = link[link.find('mobility') + len('mobility') + 1:]

        if link[-3:] == "pdf":
            path = os.path.join(directory_pdf, file_name)
            if not os.path.isfile(path):
                new_files = True
                urllib.request.urlretrieve(link, path)
                print(file_name)
                time.sleep(1)

    if not new_files:
        print('Google: No updates')
    return new_files


def build_google_report(
        source="Global_Mobility_Report.csv",
        destination="mobility_report.csv",
        report_type="regions"):
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


def download_apple_report(directory="apple_reports"):
    """Download new Apple Mobility Reports
    """
    url = "https://www.apple.com/covid19/mobility"
    session = HTMLSession()
    # Use the object above to connect to needed webpage
    resp = session.get(url)
    # Run JavaScript code on webpage
    resp.html.render(sleep=10)
    soup = BeautifulSoup(resp.html.html, "html.parser")
    button = soup.find('div', {"class": "download-button-container"}).find('a')
    link = button['href']
    new_files = False

    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = "applemobilitytrends.csv"
    if link[-3:] == "csv":
        path = os.path.join(directory, file_name)
        if not os.path.isfile(path):
            new_files = True
            urllib.request.urlretrieve(link, path)
            print(file_name)
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
    return new_files


def build_apple_report(
    source=os.path.join(
        'apple_reports',
        "applemobilitytrends.csv"),
        destination=os.path.join(
            'apple_reports',
        "apple_mobility_report.csv")):
    apple = pd.read_csv(source)
    apple = apple.drop(columns=['alternative_name'])
    subcity_country_file = os.path.join(
        'auxiliary_data', 'sub&city_country_Apple.xlsx')

    if os.path.isfile(subcity_country_file):
        subcity_country = pd.read_excel(subcity_country_file, index_col=0)
    else:
        subcity_country = None

    apple['country'] = apple.apply(lambda x: subcity_country.loc[x['region'], 'country'] if (
        x['geo_type'] != 'country/region' and subcity_country is not None and x['region'] in subcity_country.index) else x['region'], axis=1)
    apple = apple.melt(
        id_vars=[
            'geo_type',
            'region',
            'transportation_type',
            'country'],
        var_name='date')
    apple['value'] = apple['value'] - 100
    apple = apple.pivot_table(
        index=[
            "geo_type",
            "region",
            "date",
            "country"],
        columns='transportation_type').reset_index()
    apple.columns = [t + (v if v != "value" else "") for v, t in apple.columns]
    apple['subregion_and_city'] = apple.apply(lambda x: x['region'] if (
        x['geo_type'] != 'country/region') else "Total", axis=1)
    apple = apple[['country', 'subregion_and_city',
                   'geo_type', 'date', 'driving', 'transit', 'walking']]
    apple = apple.sort_values(by=['country', 'subregion_and_city', 'date'])
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
    # preprocess apple data
    apple = pd.read_csv(apple_source)
    apple = apple.drop(columns=['alternative_name'])
    subcity_country_file = os.path.join(
        'auxiliary_data', 'sub&city_country_Apple.xlsx')

    if os.path.isfile(subcity_country_file):
        subcity_country = pd.read_excel(subcity_country_file, index_col=0)
    else:
        subcity_country = None

    apple['country'] = apple.apply(lambda x: subcity_country.loc[x['region'], 'country'] if (
        x['geo_type'] != 'country/region' and subcity_country is not None and x['region'] in subcity_country.index) else x['region'], axis=1)
    apple = apple.melt(
        id_vars=[
            'geo_type',
            'region',
            'transportation_type',
            'country'],
        var_name='date')
    apple['value'] = apple['value'] - 100
    apple = apple.pivot_table(
        index=[
            "geo_type",
            "region",
            "date",
            "country"],
        columns='transportation_type').reset_index()
    apple.columns = [t + (v if v != "value" else "") for v, t in apple.columns]
    apple['sub_region_1'] = apple.apply(lambda x: x['region'] if (
        x['geo_type'] != 'country/region') else "Total", axis=1)
    apple = apple[['country', 'sub_region_1',
                   'date', 'driving', 'transit', 'walking']]

    country_AtoG_file = os.path.join(
        'auxiliary_data', 'country_Apple_to_Google.csv')

    if os.path.isfile(country_AtoG_file):
        country_AtoG = pd.read_csv(country_AtoG_file, index_col=0)
    else:
        country_AtoG = None
    apple['country'] = apple.apply(lambda x: country_AtoG.loc[x['country'], 'country_google'] if (
        country_AtoG is not None and x['country'] in country_AtoG.index) else x['country'], axis=1)
    apple['sub_region_2'] = "Total"

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


def csv_to_excel(csv_path, excel_path):
    """Helper function which create Excel file from CSV"""
    df = pd.read_csv(csv_path, low_memory=False)
    df.to_excel(excel_path, index=False, sheet_name='Data')


def run():
    """Run parse flow"""
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
        build_apple_report()
        csv_to_excel(
            os.path.join(
                'apple_reports',
                "apple_mobility_report.csv"),
            os.path.join(
                'apple_reports',
                "apple_mobility_report.xlsx"))
    # build summary report
    if new_files_status_apple or new_files_status_google:
        build_summary_report()
        csv_to_excel(
            os.path.join(
                "summary_reports",
                "summary_report.csv"),
            os.path.join(
                "summary_reports",
                "summary_report.xlsx"))


if __name__ == '__main__':
    run()
