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
from mobility_scraper.utils import *
from mobility_scraper import (
    google_mobility,
    apple_mobility,
    waze_mobility,
    tomtom_mobility,
    merge_reports,
)

import click


@exception_handler("Google")
def process_google_data():
    """Process Google mobility data

    Returns:
        bool: flag indicating whether or not new files have been downloaded
    """
    # unzip existing report
    if GOOGLE_ZIP_PATH.is_file():
        with zp.ZipFile(GOOGLE_ZIP_PATH, "r") as zf:
            zf.extract(GOOGLE_RAW_FILE, GOOGLE_DIR)
    # download new report
    new_files_status_google = download_files(GOOGLE_DIR, GOOGLE_URL, GOOGLE_RAW_FILE)
    print(update_status_message("Google", new_files_status_google))
    # build new reports
    if new_files_status_google:
        # build basic report for the worldwide
        google_world = google_mobility.build_report(GOOGLE_CSV_PATH)
        # build a report for the US
        google_US = google_mobility.build_report(GOOGLE_CSV_PATH, "US")
        # build a report for Brazil
        google_brazil = google_mobility.build_report(
            GOOGLE_CSV_PATH, report_type="regions_detailed", countries=["Brazil"]
        )
        # build detailed reports for world regions
        google_world_regions = google_mobility.build_report(
            GOOGLE_CSV_PATH,
            report_type="world_regions_detailed",
            country_regions_file=COUNTRY_WORLD_REGIONS_PATH,
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
        write_df_to_csv_and_excel(google_world, GOOGLE_REGIONS_PATHS)
        write_df_to_csv_and_excel(google_US, GOOGLE_US_PATHS)
        write_df_to_csv_and_excel(google_brazil, GOOGLE_BRAZIL_PATHS)
        write_df_to_csv_and_excel(google_europe, GOOGLE_EUROPE_PATHS)
        write_df_to_csv_and_excel(google_asia_africa, GOOGLE_ASIA_AFRICA_PATHS)
        write_df_to_csv_and_excel(google_america_oceania, GOOGLE_AMERICA_OCEANIA_PATHS)
        # zip raw report
        with zp.ZipFile(GOOGLE_ZIP_PATH, "w", zp.ZIP_DEFLATED) as zf:
            zf.write(GOOGLE_CSV_PATH, GOOGLE_RAW_FILE)
    # delete raw CSV report
    GOOGLE_CSV_PATH.unlink()
    return new_files_status_google


@exception_handler("Apple")
def process_apple_data():
    """Process Apple mobility data

    Returns:
        bool: flag indicating whether or not new files have been downloaded
    """
    new_files_status_apple = download_files(
        APPLE_DIR, apple_mobility.get_link(), APPLE_RAW_FILE
    )
    print(update_status_message("Apple", new_files_status_apple))
    if new_files_status_apple:
        # build reports
        apple_world = apple_mobility.build_report(APPLE_CSV_PATH)
        apple_US = apple_mobility.build_report(APPLE_CSV_PATH, report_type="US")
        # write reports to CSV and Excel
        write_df_to_csv_and_excel(apple_world, APPLE_WORLD_PATHS)
        write_df_to_csv_and_excel(apple_US, APPLE_US_PATHS)

    return new_files_status_apple


@exception_handler("Waze")
def process_waze_data():
    """Process Waze mobility data

    Returns:
        bool: flag indicating whether or not new files have been downloaded
    """
    new_files_status_waze = download_files(WAZE_DIR, WAZE_URLS, WAZE_RAW_FILES)
    print(update_status_message("Waze", new_files_status_waze))
    if new_files_status_waze:
        # build report
        waze = waze_mobility.build_report(WAZE_COUNTRY_LEVEL_PATH, WAZE_CITY_LEVEL_PATH)
        # write report to CSV and Excel
        write_df_to_csv_and_excel(waze, WAZE_REPORT_PATHS)

    return new_files_status_waze


@exception_handler("TomTom")
def process_tomtom_data():
    """Process TomTom mobility data

    Returns:
        bool: flag indicating whether or not new files have been downloaded
    """
    # process TomTom reports
    new_files_status_tomtom = tomtom_mobility.check_update(TOMTOM_REPORT_PATHS[".csv"])
    print(update_status_message("TomTom", new_files_status_tomtom))
    if new_files_status_tomtom:
        # scrape new data
        tomtom = tomtom_mobility.download_report(COUNTRY_ALPHA_CODES_PATH)
        write_df_to_csv_and_excel(tomtom, TOMTOM_REPORT_PATHS)

    return new_files_status_tomtom


@click.group(help="Scraper for mobility data")
def cli():
    pass


@cli.command(help="Scrape mobility data from specified sources")
@click.argument("sources", nargs=-1)
def scrape(sources):
    """Scrape mobility data from specified sources

    Args:
        sources (tuple, optional): Mobility data sources

    Returns:
        dict: status of update for all sources (Google, Apple, Waze and TomTom)
    """
    all_sources = ("google", "apple", "waze", "tomtom")
    new_files_status = {source: False for source in all_sources}
    # if no parameters are provided, scrape data from all sources
    if len(sources) == 0:
        sources = all_sources
    # process Google reports
    new_files_status["google"] = process_google_data() if "google" in sources else False
    # process Apple reports
    new_files_status["apple"] = process_apple_data() if "apple" in sources else False
    # process Waze reports
    new_files_status["waze"] = process_waze_data() if "waze" in sources else False
    # process TomTom reports
    new_files_status["tomtom"] = process_tomtom_data() if "tomtom" in sources else False
    return new_files_status


@cli.command("merge", help="Merge mobility reports (Apple and Google)")
@exception_handler("Merging")
def merge_data():
    """Merge Google and Apple reports"""
    print("Merging reports...")
    summary_regions = merge_reports.build_summary_report(
        APPLE_WORLD_PATHS[".csv"],
        GOOGLE_REGIONS_PATHS[".csv"],
        COUNTRY_APPLE_TO_GOOGLE_PATH,
        SUBREGIONS_APPLE_TO_GOOGLE_PATH,
    )
    summary_US = merge_reports.build_summary_report(
        APPLE_US_PATHS[".csv"],
        GOOGLE_US_PATHS[".csv"],
        COUNTRY_APPLE_TO_GOOGLE_PATH,
        SUBREGIONS_APPLE_TO_GOOGLE_PATH,
        "US",
    )
    summary_countries = summary_regions[summary_regions["region"] == "Total"].drop(
        columns=["region"]
    )

    print("Writing merged reports to files...")
    write_df_to_csv_and_excel(summary_regions, SUMMARY_REGIONS_PATHS)
    write_df_to_csv_and_excel(summary_US, SUMMARY_US_PATHS)
    write_df_to_csv_and_excel(summary_countries, SUMMARY_COUNTRIES_PATHS)


@cli.command(help="Scrape data from all sources and merge reports")
@click.pass_context
def run_all(ctx):
    """Run parse flow and build reports"""
    new_files_status = ctx.invoke(scrape)
    # build merged reports
    if new_files_status["apple"] or new_files_status["google"]:
        ctx.invoke(merge_data)


if __name__ == "__main__":
    cli()