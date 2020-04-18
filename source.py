import io
import os
import datetime

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession

import pandas as pd


def download_google_reports(directory_pdf="pdf_reports", directory_csv="google_reports"):
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

    for one_a_tag in soup.findAll('a', {"class": "download-link"}):
        link = one_a_tag['href']
        file_name = link[link.find('mobility') + len('mobility') + 1:]
        
        if link[-3:] == "pdf":
            path = os.path.join(directory_pdf, file_name)
            if not os.path.isfile(path):
                new_files = True
                urllib.request.urlretrieve(link, path)
                print(file_name)
                time.sleep(1)

        elif link[-3:] == "csv":
            path = os.path.join(directory_csv, file_name)
            if not os.path.isfile(path):
                new_files = True
                urllib.request.urlretrieve(link, path)
                print(file_name)
                time.sleep(1)
            else:
                path_new = os.path.join(directory_csv, file_name+"_new")
                urllib.request.urlretrieve(link, path_new)
                if os.path.getsize(path)==os.path.getsize(path_new):
                    os.remove(path_new)
                else:
                    new_files = True
                    os.remove(path)
                    os.rename(path_new, path)

    if not new_files:
        print('Google: No updates')
    return new_files


def build_google_report(source="Global_Mobility_Report.csv", destination="mobility_report.csv", report_type="regions"):
    df = pd.read_csv(source, low_memory=False)
    df = df.drop(columns=['country_region_code'])
    df = df.rename(columns={'country_region':'country', 'retail_and_recreation_percent_change_from_baseline':'retail',
                       'grocery_and_pharmacy_percent_change_from_baseline':'grocery and pharmacy',
                       'parks_percent_change_from_baseline':'parks', 
                        'transit_stations_percent_change_from_baseline':'transit stations',
                       'workplaces_percent_change_from_baseline':'workplaces', 
                       'residential_percent_change_from_baseline':'residential'})
    if report_type=="regions":
        df = df[df['sub_region_2'].isnull()]
        df = df.drop(columns=['sub_region_2'])
        df = df.rename(columns={'sub_region_1':'region'})
        df['region'].fillna('Total', inplace=True)
    elif report_type=="US":
        df = df[(df['country']=="United States")]
        df = df.drop(columns=['country'])
        df = df.rename(columns={'sub_region_1':'state', 'sub_region_2':'county'})
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
            path_new = os.path.join(directory, file_name+"_new")
            urllib.request.urlretrieve(link, path_new)
            if os.path.getsize(path)==os.path.getsize(path_new):
                os.remove(path_new)
            else:
                new_files = True
                os.remove(path)
                os.rename(path_new, path)

    if not new_files:
        print('Apple: No updates')
    return new_files


def csv_to_excel(csv_path, excel_path):
    """Helper function which create Excel file from CSV"""
    df = pd.read_csv(csv_path, low_memory=False)
    df.to_excel(excel_path, index=False, sheet_name='Data')


def run():
    """Run parse flow"""
    # parse Google reports
    new_files_status_google = download_google_reports()
    if new_files_status_google:
        build_google_report(source=os.path.join("google_reports","Global_Mobility_Report.csv"), 
                            destination=os.path.join("google_reports", "mobility_report_countries.csv"), report_type="regions")
        build_google_report(source=os.path.join("google_reports","Global_Mobility_Report.csv"), 
                            destination=os.path.join("google_reports", "mobility_report_US.csv"), report_type="US")
        csv_to_excel(os.path.join("google_reports", "mobility_report_countries.csv"),
                        os.path.join("google_reports", "mobility_report_countries.xlsx"))
        csv_to_excel(os.path.join("google_reports", "mobility_report_US.csv"),
                        os.path.join("google_reports", "mobility_report_US.xlsx"))

    new_files_status_apple = download_apple_report()
    if new_files_status_apple:
        csv_to_excel(os.path.join('apple_reports',"applemobilitytrends.csv"), os.path.join('apple_reports',"applemobilitytrends.xlsx"))


if __name__ == '__main__':
    run()
