import io
import os
import datetime

import requests
import urllib.request
import time
from bs4 import BeautifulSoup

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
    """Download new Apple mobility report"""
    last_file = [filename for filename in os.listdir(directory) if filename.endswith(".csv")][0]
    last_date = datetime.datetime.strptime("-".join(last_file.split("-")[1:])[:-4] , '%Y-%m-%d')
    next_date = last_date+datetime.timedelta(days=1)
    next_date_str = str(next_date).split(" ")[0]
    next_day_str = str(next_date.day)
    file_name = "applemobilitytrends-" + next_date_str + ".csv"
    next_url="https://covid19-static.cdn-apple.com/covid19-mobility-data/2005HotfixDev"+next_day_str +"/v1/en-us/" + file_name
    request = requests.get(next_url)
    if request.status_code == 200:
        for f in [f for f in os.listdir(directory)] :
            os.remove(os.path.join(directory, f))
        urllib.request.urlretrieve(next_url, os.path.join(directory,file_name))
        print(file_name)
        return (True, file_name[:-4])
    else:
        print("Apple: No updates")
        return (False, file_name[:-4])


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
    # download apple report (not working :-( )
    new_files_status_apple, file_name_apple = download_apple_report()
    #if new_files_status_apple:
    #csv_to_excel(os.path.join('apple_reports',file_name_apple+".csv"), os.path.join('apple_reports',file_name_apple+".xlsx"))
    csv_to_excel(os.path.join('apple_reports',"applemobilitytrends-2020-04-15.csv"), os.path.join('apple_reports',"applemobilitytrends-2020-04-15.xlsx"))
if __name__ == '__main__':
    run()
