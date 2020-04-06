# Scraper of Google COVID-19 Community Mobility Reports
This is a repository with a data scraper of Community Mobility Reports and reports in different formats.

## How to run script
```bash
pip install requirements.txt
python source.py
```
## Repository structure
------------

    ├── README.md                   <- The top-level README for developers using this project.
    ├── data
    │   ├── PDF files               <- PDF files which scraped from Google site of Community Mobility Reports
    │
    ├── jupyter notebook
    │   ├── Scraper of Google COVID-19 Community Mobility Reports.ipynb      <- Jupyter notebook with a scraper 
    │   ├── codes.csv               <- table with 2-letter codes of countries
    │   ├── mobility_*.xlsx/.csv    <- scraped reports in different formats
    │
    ├── codes.csv                   <- table with 2-letter codes of countries
    │
    ├── mobility_report_US.csv      <- detailed scraped report for the US in CSV format
    │
    ├── mobility_report_regions.csv <- detailed scraped report of regions in CSV format
    │
    ├── report_source.txt           <- files on which current scraped reports were created
    │
    ├── requirements.txt            <- the requirements file for reproducing the code
    │
    └── source.py                   <- Source code for use in this project.

--------

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## TODO
1. Optimize parse flow
2. Add feature of scraping time-series data from graphs

## Dashboards based on these data
1. [Dashboard for the US -1](https://public.tableau.com/profile/karl3594#!/vizhome/State-by-StateCOVID-19MobilityChanges/ChangesbyState)
2. [Dashboard for the US -2](https://public.tableau.com/profile/sky.quintin#!/vizhome/Mobilitydata/CommunityMobility)
3. [Here can be your great dashboard/visualization]
