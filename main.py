"""
This script loads Google, Apple, Waze and TomTom Mobility reports, builds cleaned reports in different formats and builds merged files from these sources.

Original data:
    - Google Community Mobility reports: https://www.google.com/covid19/mobility/
    - Apple Mobility Trends reports: https://www.apple.com/covid19/mobility
    - Waze COVID-19 local driving trends: https://www.waze.com/covid19
    - TomTom Traffic Index: https://www.tomtom.com/en_gb/traffic-index/ranking/

"""
import zipfile as zp

from mobility_scraper.paths_and_URLs import *
from mobility_scraper.download_files import *
from mobility_scraper import google_mobility

if __name__ == "__main__":
    # process Google reports
    # unzip existing report
    if GOOGLE_ZIP_PATH.is_file():
        with zp.ZipFile(GOOGLE_ZIP_PATH, "r") as zf:
            zf.extract(GOOGLE_RAW_FILE, GOOGLE_DIR)
    # download new report
    new_files_status_google = download_files(GOOGLE_DIR, GOOGLE_URL, GOOGLE_RAW_FILE)
    print(update_status_message('Google', new_files_status_google))
    # build new reports
    if new_files_status_google:
        # build basic report for the worldwide
        google_world = google_mobility.build_report(GOOGLE_CSV_PATH)
        # build a report for the US
        google_US = google_mobility.build_report(GOOGLE_CSV_PATH, "US")
        # build a report for Brazil
        google_brazil = google_mobility.build_report(GOOGLE_CSV_PATH, 
            report_type="regions_detailed", countries=["Brazil"]
        )
        # build detailed reports for world regions
        google_world_regions = google_mobility.build_report(GOOGLE_CSV_PATH, 
            report_type="world_regions_detailed",
            country_regions_file = COUNTRY_WORLD_REGIONS_PATH
        )
        google_europe = google_world_regions[
            google_world_regions.world_region.isin(["Europe"])
        ]
        google_asia_africa = google_world_regions[
            google_world_regions.world_region.isin(["Asia", "Africa"])
        ]
        google_america_oceania = google_world_regions[
            google_world_regions.world_region.isin(
                ["South America", "North America", "Oceania"]
            )
        ]
        # write reports to CSV and Excel
        google_world.to_csv(GOOGLE_REGIONS_PATHS[".csv"], index=False)
        google_world.to_excel(
            GOOGLE_REGIONS_PATHS[".xlsx"],
            index=False,
            sheet_name="Data",
            engine="xlsxwriter",
        )
        google_US.to_csv(
            GOOGLE_US_PATHS[".csv"], index=False
        )
        google_US.to_excel(
            GOOGLE_US_PATHS[".xlsx"],
            index=False,
            sheet_name="Data",
            engine="xlsxwriter",
        )
        google_brazil.to_csv(
            GOOGLE_BRAZIL_PATHS[".csv"], index=False
        )
        google_brazil.to_excel(
            GOOGLE_BRAZIL_PATHS[".xlsx"],
            index=False,
            sheet_name="Data",
            engine="xlsxwriter",
        )
        google_europe.to_csv(
            GOOGLE_EUROPE_PATHS[".csv"], index=False
        )
        google_europe.to_excel(
            GOOGLE_EUROPE_PATHS[".xlsx"],
            index=False,
            sheet_name="Data",
            engine="xlsxwriter",
        )
        google_asia_africa.to_csv(
            GOOGLE_ASIA_AFRICA_PATHS[".csv"],
            index=False,
        )
        google_asia_africa.to_excel(
            GOOGLE_ASIA_AFRICA_PATHS[".xlsx"],
            index=False,
            sheet_name="Data",
            engine="xlsxwriter",
        )
        google_america_oceania.to_csv(
            GOOGLE_AMERICA_OCEANIA_PATHS[".csv"],
            index=False,
        )
        google_america_oceania.to_excel(
            GOOGLE_AMERICA_OCEANIA_PATHS[".xlsx"],
            index=False,
            sheet_name="Data",
            engine="xlsxwriter",
        )
            # zip raw report
        with zp.ZipFile(GOOGLE_ZIP_PATH, "w", zp.ZIP_DEFLATED) as zf:
            zf.write(GOOGLE_CSV_PATH, GOOGLE_RAW_FILE)
    # delete raw CSV report
    GOOGLE_CSV_PATH.unlink()
    # process Apple reports
    # new_files_status_apple = download_files(APPLE_DIR, get_apple_link(), APPLE_RAW_FILE)
    # print(update_status_message('Apple', new_files_status_apple))
    
