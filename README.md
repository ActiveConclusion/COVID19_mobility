# Scraper of Google COVID-19 Community Mobility Reports
This is a repository with a data scraper of Community Mobility Reports and reports in different formats.

## About Google COVID-19 Community Mobility Reports
In early April 2020, Google started publishing an early release of our COVID-19 Community Mobility Reports to provide insights into what has changed in response to work from home, shelter in place, and other policies aimed at flattening the curve of this pandemic. These reports have been developed to be helpful while adhering to our stringent privacy protocols and policies. 

These Community Mobility Reports aim to provide insights into what has changed in response to policies aimed at combating COVID-19. The reports chart movement trends over time by geography, across different categories of places such as retail and recreation, groceries and pharmacies, parks, transit stations, workplaces, and residential.

## Data explorer
[All downloaded reports in PDF format](data)

Data by regions: [Google sheets](https://docs.google.com/spreadsheets/d/1fuV8AKwSjIh9Pswb_XTC0UFaoFPMBbz9YHAZ8TScAQc/edit#gid=1171841841), [CSV](mobility_report_regions.csv), [Excel](jupyter%20notebook/mobility_report_regions.xlsx)

Data for the US: [Google sheets](https://docs.google.com/spreadsheets/d/1pxuTu10uO7MsBaKA554XSuCpnF--FTqwdnl_sUHfWro/edit#gid=265926435), [CSV](mobility_report_US.csv), [Excel](jupyter%20notebook/mobility_report_US.csv)

## How to run script
```bash
pip install -r requirements.txt
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
    │   ├── mobility_*.xlsx/.csv    <- scraped reports in different formats
    │
    ├── codes.csv                   <- table with 2-letter codes of countries (must be for running the script)
    │
    ├── mobility_report_US.csv      <- detailed scraped report for the US in CSV format
    │
    ├── mobility_report_regions.csv <- detailed scraped report of regions in CSV format
    │
    ├── report_source.txt           <- files on which current scraped reports were created
    │
    ├── requirements.txt            <- the requirements file for reproducing the code
    │
    └── source.py                   <- source code for use in this project

--------

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 

[Place to discuss use cases for this data](https://github.com/ActiveConclusion/COVID19_mobility/issues/4)

## Dashboards based on these data
1. [Dashboard for the US-1](https://public.tableau.com/profile/karl3594#!/vizhome/State-by-StateCOVID-19MobilityChanges/ChangesbyState)
2. [Dashboard for the US-2](https://public.tableau.com/profile/sky.quintin#!/vizhome/Mobilitydata/CommunityMobility)
3. [Dashboard for the world](https://public.tableau.com/profile/ryansoares#!/vizhome/COVID-19CommunityMobility/Dashboard1)
4. [Here can be your great dashboard/visualization]
