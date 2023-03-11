<a href="https://www.buymeacoffee.com/AConclusion" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
# COVID-19 Mobility Data Aggregator. Scraper of Google, Apple, Waze and TomTom COVID-19 Mobility Reports
This is a repository with a data scraper of Mobility Reports and reports in different formats.

## Table of contents
1. [ About data ](#about-data)
    * [ 1. About Google COVID-19 Community Mobility Reports](#about-google-covid-19-community-mobility-reports)
    * [ 2. About Apple COVID-19 Mobility Trends Reports](#about-apple-covid-19-mobility-trends-reports)
    * [ 3. About Waze COVID-19 local driving trends](#about-waze-covid-19-local-driving-trends)
    * [ 4. About TomTom Trafic Index](#about-tomtom-traffic-index)
2. [ Data explorer ](#data-explorer)
    * [ 1. Google Reports](#google-reports)
    * [ 2. Apple Reports](#apple-reports)
    * [ 3. Waze Reports](#waze-reports)
    * [ 4. TomTom Reports](#tomtom-reports)
    * [ 5. Summary Reports](#summary-reports)
3. [ How to run script ](#how-to-run-script)
    * [ 1. Installation](#installation)
    * [ 2. Usage](#usage)
4. [ Contributing ](#contributing)
5. [ Showcases ](#showcases)
    * [ 1. Dashboards and visualizations based on these data](#dashboards-and-visualizations-based-on-these-data)
    * [ 2. Articles and research publications](#articles-and-research-publications)

## About data

### About [Google COVID-19 Community Mobility Reports](https://www.google.com/covid19/mobility/)
In early April 2020, Google started publishing an early release of COVID-19 Community Mobility Reports to provide insights into what has changed in response to work from home, shelter in place, and other policies aimed at flattening the curve of this pandemic. These reports have been developed to be helpful while adhering to our stringent privacy protocols and policies. 

These Community Mobility Reports aim to provide insights into what has changed in response to policies aimed at combating COVID-19. The reports chart movement trends over time by geography, across different categories of places such as retail and recreation, groceries and pharmacies, parks, transit stations, workplaces, and residential.

**Update interval:** The Community Mobility Reports are no longer being updated as of 2022-10-15.

By downloading or using this data and reports, you agree to Google [Terms of Service](https://policies.google.com/terms).

### About [Apple COVID-19 Mobility Trends Reports](https://www.apple.com/covid19/mobility)
The CSV file shows a relative volume of directions requests per country/region or city compared to a baseline volume on January 13th, 2020.

Day defined as midnight-to-midnight, Pacific time. Cities represent usage in greater metropolitan areas and are stably defined during this period. In many countries/regions and cities, relative volume has increased since January 13th, consistent with normal, seasonal usage of Apple Maps. Day of week effects are important to normalize as you use this data.

Data that is sent from users' devices to the Maps service is associated with random, rotating identifiers so Apple doesn't have a profile of your movements and searches. Apple Maps has no demographic information about Apple users, so it's impossible to make any statements about the representativeness of usage against the overall population.

**Update interval:** As of April 14, 2022, Apple is no longer providing COVID-19 mobility trends reports.

By downloading or using this data, you agree to Apple terms.


### About [Waze COVID-19 local driving trends](https://www.waze.com/covid19)
The driven kilometers/miles percent change data being shared comes from the Waze app and is aggregated and anonymized. These insights were generated using differential privacy to protect user privacy. No personally identifiable information, such as an individual’s location, contacts, or movement, is available through this data. 

These reports show the increase or decrease in driven kilometers/miles as a percent change compared to a baseline. The changes for each day are compared to a baseline value for that day of the week. 
* The baseline is the average value, for the corresponding day of the week, during the 2- week period February 11, 2020 to February 25, 2020. 
* The reports show trends over two weeks with the most recent data representing approximately 2-3 days ago. 

As with all samples, this may or may not represent the exact behavior of a wider population.

**Update interval:** Waze dashboard has been retired and will no longer be updated as of July 2022


### About [TomTom Traffic Index](https://www.tomtom.com/en_gb/traffic-index)
Covering 416 cities across 57 countries on 6 continents, Traffic Index ranks urban congestion worldwide and provides free access to city-by-city information.
Wondering how we determine the rankings, and what exactly the percentages mean?

A 53% congestion level in Bangkok, for example, means that a 30-minute trip will take 53% more time than it would during Bangkok’s baseline uncongested conditions.

You can turn this 53% into travel time through simple calculations.
First: 0.53 x 30 mins = 15.9 mins extra average travel time.
Second: 30 mins + 15.9 mins = 45.9 mins total average travel time.

We calculate the baseline per city by analyzing free-flow travel times of all vehicles on the entire road network – recorded 24/7, 365 days a year. This information allows us to also calculate, for example, how much extra time a driver will spend in traffic during rush hour in Bangkok.

We perform calculations for all hours of each day, so you can see congestion levels at any time in any city, including morning and evening peak hours.

**Update interval:** daily

## Data explorer

### Google reports:
[Raw CSV file](google_reports/Global_Mobility_Report.zip) (in ZIP archive). Direct link to the original CSV: https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv

Data for the worldwide (only 1st level of subregions): [CSV](google_reports/mobility_report_countries.csv), [Excel](google_reports/mobility_report_countries.xlsx)

**Detailed reports:**

Data for the US: [CSV](google_reports/mobility_report_US.csv), [Excel](google_reports/mobility_report_US.xlsx)

Data for Brazil: [CSV](google_reports/mobility_report_brazil.csv), [Excel](google_reports/mobility_report_brazil.xlsx)

Data for Europe: [CSV](google_reports/mobility_report_europe.zip) (in ZIP archive), [Excel](google_reports/mobility_report_europe.xlsx)

Data for Asia + Africa: [CSV](google_reports/mobility_report_asia_africa.csv), [Excel](google_reports/mobility_report_asia_africa.xlsx)

Data for North and South America + Oceania (Brazil and US excluded): [CSV](google_reports/mobility_report_america_oceania.csv), [Excel](google_reports/mobility_report_america_oceania.xlsx)

### Apple reports:
[Raw CSV file](apple_reports/applemobilitytrends.csv)

Data for the worldwide: [CSV](apple_reports/apple_mobility_report.csv), [Excel](apple_reports/apple_mobility_report.xlsx)

Data for the US: [CSV](apple_reports/apple_mobility_report_US.csv), [Excel](apple_reports/apple_mobility_report_US.xlsx)

The following transformations have been made here:

* transformed dates from columns to rows
* transformed transportation types from rows to columns
* subtracted 100 from values (such as in Google Mobility Reports)

**Note: Data for May 11-12, 2020 and March 12, 2021 is not available**

### Waze reports:
Raw CSV files: [Country-level](waze_reports/Waze_Country-Level_Data.csv), [City-level](waze_reports/Waze_City-Level_Data.csv)

Preprocessed report: [Google Sheets](https://docs.google.com/spreadsheets/d/1prxgtL1s8AvJDQb0hF2_g8rswwZElKQc2K79-FOmmt8/edit?usp=sharing), [CSV](waze_reports/waze_mobility.csv), [Excel](waze_reports/waze_mobility.xlsx)

### TomTom reports:
Scraped reports: [Google Sheets](https://docs.google.com/spreadsheets/d/1aAdXeAhu3Mx9dbFQN_mgc2bXSV61jFbgGzcF_oAUK5Q/edit#gid=0), [CSV](tomtom_reports/tomtom_trafic_index.csv), [Excel](tomtom_reports/tomtom_trafic_index.xlsx)

diffRatio attribute shows relative difference of average congestion levels in 2020 from standard congestion levels in 2019.

**Note: Data for China only available up to 21.02.2021**

### Summary reports:
These are merged Apple and Google reports.

Report by regions: [CSV](summary_reports/summary_report_regions.csv), [Excel](summary_reports/summary_report_regions.xlsx)

Report by countries: [Google Sheets](https://docs.google.com/spreadsheets/d/1d9t7xg-lUPEUArTsc_wMOGl1XfzpXmeWcALx7v58KcU), [CSV](summary_reports/summary_report_countries.csv), [Excel](summary_reports/summary_report_countries.xlsx)

Report for the US: [CSV](summary_reports/summary_report_US.csv), [Excel](summary_reports/summary_report_US.csv)

## How to run script
### Installation
```bash
git clone https://github.com/ActiveConclusion/COVID19_mobility
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
Also, available [Jupyter notebook](notebooks/Scraper%202.0.ipynb) mirror of this script

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 

[Place to discuss use cases for this data](https://github.com/ActiveConclusion/COVID19_mobility/issues/4)

## Showcases
### Dashboards and visualizations based on these data
1. [Dashboard for the US-1](https://public.tableau.com/profile/karl3594#!/vizhome/State-by-StateCOVID-19MobilityChanges/ChangesbyState)
2. [Dashboard for the US-2](https://public.tableau.com/profile/sky.quintin#!/vizhome/Mobilitydata/CommunityMobility)
3. [Dashboard for the world](https://public.tableau.com/profile/ryansoares#!/vizhome/COVID-19CommunityMobility/Dashboard1)
4. [Balefire COVID-19 USA Data Explorer](http://balefire.info/)
5. [Pandemic Traffic in Ireland](https://public.tableau.com/profile/docinsight#!/vizhome/COVIDtrafficinIrelandrepoint/MobilityDashboard) by David ó Cinnéide
6. [New South Wales COVID Tracking Dashboard](https://public.tableau.com/profile/damjan.vlastelica#!/vizhome/CovidNSWTracker/HomeDash?publish=yes) by Damjan Vlastelica
7. [Global COVID Vital Signs](https://eastnileuc.shinyapps.io/global_covidts/)
8. [Toronto After The First Wave. Mobility Dashboard](https://torontoafterthefirstwave.com/dashboards/mobility/)
9. [Here can be your great dashboard/visualization]

### Articles and research publications
1. [Is Your Community Doing Enough To Fight COVID-19?](https://towardsdatascience.com/is-your-community-doing-enough-to-fight-covid-19-aa745b424eb1) by [Molly Liebeskind](https://towardsdatascience.com/@molly.liebeskind)
2. [Project US Mobility and Fuel Demand Under COVID-19](https://covid19-mobility.com)
3. [COVID-19: Country progress tracker and forward projections](https://www.agility.asia/covid) 
4. [Krekel, C., Swanke, S., De Neve, J., & Fancourt, D. (2020). Are Happier People More Compliant? Global Evidence From Three Large-Scale Surveys During Covid-19 Lockdowns](http://ftp.iza.org/dp13690.pdf)
5. [Green shoots and mobility: Philippine economic prospects By Diwa C. Guinigundo](https://www.bworldonline.com/green-shoots-and-mobility-philippine-economic-prospects/)
6. [Franks J, Gruss B, Mulas-Granados C, Patnam M, Weber S. Reopening strategies, mobility and COVID-19 infections in Europe: panel data analysis. BMJ Open. 2022;12(2):e055938. Published 2022 Feb 9. doi:10.1136/bmjopen-2021-055938](https://bmjopen.bmj.com/content/12/2/e055938)
7. [Anna Godøy, Maja Weemes Grøtting. Implementation and economic effects of local non-pharmaceutical interventions. medRxiv 2022.02.10.22270783; doi:https://doi.org/10.1101/2022.02.10.22270783](https://www.medrxiv.org/content/10.1101/2022.02.10.22270783v1.full)
8. [Strzelecki, A.; Azevedo, A.; Rizun, M.; Rutecka, P.; Zagała, K.; Cicha, K.; Albuquerque, A. Human Mobility Restrictions and COVID-19 Infection Rates: Analysis of Mobility Data and Coronavirus Spread in Poland and Portugal. Int. J. Environ. Res. Public Health 2022, 19, 14455. https://doi.org/10.3390/ijerph192114455](https://www.mdpi.com/1660-4601/19/21/14455/pdf) 
9. [Bublyk, M., Feshchyn, V., Bekirova, L., & Khomuliak, O. (2022). Sustainable Development by a Statistical Analysis of Country Rankings by the Population Happiness Level. COLINS.](https://ceur-ws.org/Vol-3171/paper61.pdf) 
10. [Here can be your great article/research publication/paper]
