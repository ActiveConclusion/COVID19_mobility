"""
This script loads Google, Apple, Waze and TomTom Mobility reports, builds cleaned reports in different formats and builds merged files from these sources.

Original data:
    - Google Community Mobility reports: https://www.google.com/covid19/mobility/
    - Apple Mobility Trends reports: https://www.apple.com/covid19/mobility
    - Waze COVID-19 local driving trends: https://www.waze.com/covid19
    - TomTom Traffic Index: https://www.tomtom.com/en_gb/traffic-index/ranking/

"""
from mobility_scraper.paths_and_URLs import *

if __name__ == "__main__":
    print(GOOGLE_URL)
    
