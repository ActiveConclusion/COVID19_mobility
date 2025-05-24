<p align="center">
  <a href="https://www.buymeacoffee.com/AConclusion" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
</p>

# COVID-19 Mobility Data Aggregator (Archived)

## ⚠️ Project Status: Archived ⚠️

**This project is no longer actively maintained, and the data reports within this repository are NOT being updated.**

* **Google Reports:** Last updated by Google on 2022-10-15.
* **Apple Reports:** Last updated by Apple on 2022-04-14.
* **Waze Reports:** Last updated by Waze around July 2022.
* **TomTom Reports:** While TomTom continues to update their index, this project's scraper for TomTom data is archived. The historical data collected here remains available.

This repository preserves the data and tools used to aggregate these reports.

## Project Overview

This repository originally served as an automated scraper and data aggregator for key COVID-19 mobility reports from Google, Apple, Waze, and TomTom. As these official reports were discontinued or changed, this project transitioned into an **archive of historical mobility data** spanning from early 2020 to mid/late 2022.

The collected datasets provide valuable insights into human mobility patterns during the COVID-19 pandemic and can be used for:
* Academic research and historical analysis
* Understanding the impact of public health interventions
* Developing retrospective models

## Table of Contents

1.  [About the Original Data Sources](#about-the-original-data-sources)
    * [Google COVID-19 Community Mobility Reports](#google-covid-19-community-mobility-reports)
    * [Apple COVID-19 Mobility Trends Reports](#apple-covid-19-mobility-trends-reports)
    * [Waze COVID-19 Local Driving Trends](#waze-covid-19-local-driving-trends)
    * [TomTom Traffic Index](#tomtom-traffic-index)
2.  [Available Datasets](#available-datasets)
    * [Google Reports Data](#google-reports-data)
    * [Apple Reports Data](#apple-reports-data)
    * [Waze Reports Data](#waze-reports-data)
    * [TomTom Reports Data](#tomtom-reports-data)
    * [Summary Reports Data](#summary-reports-data)
3.  [Using the Original Scraper Scripts](#using-the-original-scraper-scripts)
    * [Installation](#installation)
    * [Usage](#usage)
4.  [Contributing](#contributing)
5.  [Showcases](#showcases)
    * [Dashboards and Visualizations](#dashboards-and-visualizations-based-on-these-data)
    * [Articles and Research Publications](#articles-and-research-publications)

## About the Original Data Sources

This section details the data sources that were aggregated by this project. Note the archival status for each.

### Google COVID-19 Community Mobility Reports
* **Source:** [google.com/covid19/mobility](https://www.google.com/covid19/mobility/)
* **Description:** Google published these reports to show movement trends over time by geography, across categories like retail, parks, transit, workplaces, and residential areas.
* **Archival Status:** Google stopped updating these reports on **2022-10-15**.
* **Terms:** By using this data, you agree to Google's [Terms of Service](https://policies.google.com/terms).

### Apple COVID-19 Mobility Trends Reports
* **Source:** [apple.com/covid19/mobility](https://www.apple.com/covid19/mobility)
* **Description:** Apple provided CSV data showing relative volume of direction requests compared to a baseline from January 13th, 2020.
* **Archival Status:** Apple stopped providing these reports on **April 14, 2022**.
* **Terms:** By using this data, you agree to Apple's terms.

### Waze COVID-19 Local Driving Trends
* **Source:** [waze.com/covid19](https://www.waze.com/covid19)
* **Description:** Waze shared aggregated, anonymized data on driven kilometers/miles as a percent change compared to a baseline (Feb 11-25, 2020).
* **Archival Status:** The Waze dashboard was retired and stopped updating in **July 2022**.

### TomTom Traffic Index
* **Source:** [tomtom.com/en_gb/traffic-index](https://www.tomtom.com/en_gb/traffic-index)
* **Description:** Ranks urban congestion worldwide, showing how much extra travel time is caused by congestion compared to baseline free-flow conditions.
* **Archival Status:** TomTom continues to update their index. However, the scraper scripts in *this repository* are archived. The historical data collected by this project remains available.

## Available Datasets

Access the collected and processed data files stored within this repository.

### Google Reports Data
* **Raw Global CSV (ZIP):** [`google_reports/Global_Mobility_Report.zip`](google_reports/Global_Mobility_Report.zip)
    * Original direct link: `https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv`
* **Worldwide (1st level subregions):**
    * [`google_reports/mobility_report_countries.csv`](google_reports/mobility_report_countries.csv)
    * [`google_reports/mobility_report_countries.xlsx`](google_reports/mobility_report_countries.xlsx)
* **Detailed Regional Reports:**
    * US: [`mobility_report_US.csv`](google_reports/mobility_report_US.csv), [`mobility_report_US.xlsx`](google_reports/mobility_report_US.xlsx)
    * Brazil: [`mobility_report_brazil.csv`](google_reports/mobility_report_brazil.csv), [`mobility_report_brazil.xlsx`](google_reports/mobility_report_brazil.xlsx)
    * Europe (ZIP CSV): [`mobility_report_europe.zip`](google_reports/mobility_report_europe.zip), Excel: [`mobility_report_europe.xlsx`](google_reports/mobility_report_europe.xlsx)
    * Asia + Africa: [`mobility_report_asia_africa.csv`](google_reports/mobility_report_asia_africa.csv), [`mobility_report_asia_africa.xlsx`](google_reports/mobility_report_asia_africa.xlsx)
    * North & South America + Oceania (Brazil & US excluded): [`mobility_report_america_oceania.csv`](google_reports/mobility_report_america_oceania.csv), [`mobility_report_america_oceania.xlsx`](google_reports/mobility_report_america_oceania.xlsx)

### Apple Reports Data
* **Raw CSV:** [`apple_reports/applemobilitytrends.csv`](apple_reports/applemobilitytrends.csv)
* **Processed Worldwide:**
    * [`apple_reports/apple_mobility_report.csv`](apple_reports/apple_mobility_report.csv)
    * [`apple_reports/apple_mobility_report.xlsx`](apple_reports/apple_mobility_report.xlsx)
* **Processed US:**
    * [`apple_reports/apple_mobility_report_US.csv`](apple_reports/apple_mobility_report_US.csv)
    * [`apple_reports/apple_mobility_report_US.xlsx`](apple_reports/apple_mobility_report_US.xlsx)
* **Notes on Apple Data Processing:**
    * Dates were transformed from columns to rows.
    * Transportation types were pivoted from rows to columns.
    * Values were reduced by 100 (to align with Google Mobility Reports format).
    * Data for May 11-12, 2020, and March 12, 2021, is unavailable.

### Waze Reports Data
* **Raw CSVs:**
    * Country-level: [`waze_reports/Waze_Country-Level_Data.csv`](waze_reports/Waze_Country-Level_Data.csv)
    * City-level: [`waze_reports/Waze_City-Level_Data.csv`](waze_reports/Waze_City-Level_Data.csv)
* **Preprocessed Report:**
    * Google Sheets: [Link](https://docs.google.com/spreadsheets/d/1prxgtL1s8AvJDQb0hF2_g8rswwZElKQc2K79-FOmmt8/edit?usp=sharing)
    * CSV: [`waze_reports/waze_mobility.csv`](waze_reports/waze_mobility.csv)
    * Excel: [`waze_reports/waze_mobility.xlsx`](waze_reports/waze_mobility.xlsx)

### TomTom Reports Data
* **Scraped Reports:**
    * Google Sheets: [Link](https://docs.google.com/spreadsheets/d/1aAdXeAhu3Mx9dbFQN_mgc2bXSV61jFbgGzcF_oAUK5Q/edit#gid=0)
    * CSV: [`tomtom_reports/tomtom_trafic_index.csv`](tomtom_reports/tomtom_trafic_index.csv)
    * Excel: [`tomtom_reports/tomtom_trafic_index.xlsx`](tomtom_reports/tomtom_trafic_index.xlsx)
* **Note:** `diffRatio` attribute shows the relative difference of average congestion levels in 2020 from 2019. Data for China in these scraped reports is only available up to 2021-02-21.

### Summary Reports Data
Merged data from Apple and Google reports.
* **By Regions:**
    * [`summary_reports/summary_report_regions.csv`](summary_reports/summary_report_regions.csv)
    * [`summary_reports/summary_report_regions.xlsx`](summary_reports/summary_report_regions.xlsx)
* **By Countries:**
    * Google Sheets: [Link](https://docs.google.com/spreadsheets/d/1d9t7xg-lUPEUArTsc_wMOGl1XfzpXmeWcALx7v58KcU)
    * CSV: [`summary_reports/summary_report_countries.csv`](summary_reports/summary_report_countries.csv)
    * Excel: [`summary_reports/summary_report_countries.xlsx`](summary_reports/summary_report_countries.xlsx)
* **For the US:**
    * [`summary_reports/summary_report_US.csv`](summary_reports/summary_report_US.csv)
    * [`summary_reports/summary_report_US.xlsx`](summary_reports/summary_report_US.xlsx)


## Using the Original Scraper Scripts

These instructions are for running the scraper scripts as they were. Be aware that the original data sources may have changed or are no longer accessible, so these scripts are primarily for historical reference or to understand the data collection methodology.

### Installation
A Python 3.x environment is required. Using a virtual environment is highly recommended:
```bash
# Clone the repository
git clone [https://github.com/ActiveConclusion/COVID19_mobility.git](https://github.com/ActiveConclusion/COVID19_mobility.git)
cd COVID19_mobility

# Create and activate a virtual environment (optional but recommended)
# python -m venv venv
# source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### Usage
```bash
# scrape data from specified sources. If no sources are provided, data will be scraped from all available sources
python scraper.py scrape <SOURCES>

# merge mobility reports (Apple and Google)
python scraper.py merge

# Scrape data from all sources and merge reports
python scraper.py run-all
```
A [Jupyter notebook version](notebooks/Scraper%202.0.ipynb) of the scraper logic is also available for review.

## Contributing

Even though this project is archived, your input is still valuable:
* **Report Issues:** If you find inaccuracies in the archived data or problems with the scraper scripts (even for historical context).
* **Share Your Work:** If you use this data for research, analysis, or visualizations, please consider adding it to the "Showcases" section!
* **Improve Documentation:** Suggestions for clarifying this README or other documentation are welcome.

Please [open an issue](https://github.com/ActiveConclusion/COVID19_mobility/issues) to discuss changes or report problems. The original discussion thread for use cases is [here](https://github.com/ActiveConclusion/COVID19_mobility/issues/4).

## Showcases

A collection of dashboards, visualizations, articles, and research that have utilized the data from this aggregator.

### Dashboards and Visualizations Based on These Data
1.  [State-by-State COVID-19 Mobility Changes by Karl E](https://public.tableau.com/profile/karl3594#!/vizhome/State-by-StateCOVID-19MobilityChanges/ChangesbyState)
2.  [State by state mobility trends](https://public.tableau.com/profile/sky.quintin#!/vizhome/Mobilitydata/CommunityMobility)
3.  [COVID-19 Community Mobility by Ryan Soares](https://public.tableau.com/profile/ryansoares#!/vizhome/COVID-19CommunityMobility/Dashboard1)
4.  [Balefire COVID-19 USA Data Explorer](http://balefire.info/)
5.  [Pandemic Traffic in Ireland](https://public.tableau.com/profile/docinsight#!/vizhome/COVIDtrafficinIrelandrepoint/MobilityDashboard) by David ó Cinnéide
6.  [New South Wales COVID Tracking Dashboard](https://public.tableau.com/profile/damjan.vlastelica#!/vizhome/CovidNSWTracker/HomeDash?publish=yes) by Damjan Vlastelica
7.  [Global COVID Vital Signs](https://eastnileuc.shinyapps.io/global_covidts/)
8.  [Toronto After The First Wave. Mobility Dashboard](https://torontoafterthefirstwave.com/dashboards/mobility/)
9.  ✨ *Your great dashboard/visualization could be here! Please [open an issue or pull request](https://github.com/ActiveConclusion/COVID19_mobility/issues) to add it.*

### Articles and research publications
1.  [Is Your Community Doing Enough To Fight COVID-19?](https://towardsdatascience.com/is-your-community-doing-enough-to-fight-covid-19-aa745b424eb1) by [Molly Liebeskind](https://towardsdatascience.com/@molly.liebeskind)
2.  [Project US Mobility and Fuel Demand Under COVID-19](https://covid19-mobility.com)
3.  [COVID-19: Country progress tracker and forward projections](https://www.agility.asia/covid)
4.  Krekel, C., Swanke, S., De Neve, J., & Fancourt, D. (2020). [*Are Happier People More Compliant? Global Evidence From Three Large-Scale Surveys During Covid-19 Lockdowns*](http://ftp.iza.org/dp13690.pdf).
5.  Guinigundo, D. C. [*Green shoots and mobility: Philippine economic prospects*](https://www.bworldonline.com/green-shoots-and-mobility-philippine-economic-prospects/).
6.  Franks J, Gruss B, Mulas-Granados C, et al. (2022). [*Reopening strategies, mobility and COVID-19 infections in Europe: panel data analysis*](https://bmjopen.bmj.com/content/12/2/e055938). BMJ Open. doi:10.1136/bmjopen-2021-055938
7.  Godøy, A., Weemes Grøtting, M. (2022). [*Implementation and economic effects of local non-pharmaceutical interventions*](https://www.medrxiv.org/content/10.1101/2022.02.10.22270783v1.full). medRxiv. doi:https://doi.org/10.1101/2022.02.10.22270783
8.  Strzelecki, A., Azevedo, A., Rizun, M., et al. (2022). [*Human Mobility Restrictions and COVID-19 Infection Rates: Analysis of Mobility Data and Coronavirus Spread in Poland and Portugal*](https://www.mdpi.com/1660-4601/19/21/14455/pdf). Int. J. Environ. Res. Public Health. https://doi.org/10.3390/ijerph192114455
9.  Bublyk, M., Feshchyn, V., Bekirova, L., & Khomuliak, O. (2022). [*Sustainable Development by a Statistical Analysis of Country Rankings by the Population Happiness Level*](https://ceur-ws.org/Vol-3171/paper61.pdf). COLINS.
10. ✨ *Your article/research could be featured here! Please [open an issue or pull request](https://github.com/ActiveConclusion/COVID19_mobility/issues) to share your work.*
