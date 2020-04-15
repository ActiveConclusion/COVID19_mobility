# Scraper of Google and Apple COVID-19 Community Mobility Reports
This is a repository with a data scraper of Community Mobility Reports and reports in different formats.

## About Google COVID-19 Community Mobility Reports
In early April 2020, Google started publishing an early release of COVID-19 Community Mobility Reports to provide insights into what has changed in response to work from home, shelter in place, and other policies aimed at flattening the curve of this pandemic. These reports have been developed to be helpful while adhering to our stringent privacy protocols and policies. 

These Community Mobility Reports aim to provide insights into what has changed in response to policies aimed at combating COVID-19. The reports chart movement trends over time by geography, across different categories of places such as retail and recreation, groceries and pharmacies, parks, transit stations, workplaces, and residential.

## About Apple COVID-19 Community Mobility Reports
The CSV file shows a relative volume of directions requests per country/region or city compared to a baseline volume on January 13th, 2020.

Day defined as midnight-to-midnight, Pacific time. Cities represent usage in greater metropolitan areas and are stably defined during this period. In many countries/regions and cities, relative volume has increased since January 13th, consistent with normal, seasonal usage of Apple Maps. Day of week effects are important to normalize as you use this data.

Data that is sent from users’ devices to the Maps service is associated with random, rotating identifiers so Apple doesn’t have a profile of your movements and searches. Apple Maps has no demographic information about Apple users, so it's impossible to make any statements about the representativeness of usage against the overall population.

## Data explorer
**Google reports:**

[All downloaded reports in PDF format](data)

Data by regions: [Google sheets](https://docs.google.com/spreadsheets/d/1fuV8AKwSjIh9Pswb_XTC0UFaoFPMBbz9YHAZ8TScAQc/edit#gid=1171841841), [CSV](google_reports/mobility_report_regions.csv), [Excel](google_reports/mobility_report_regions.xlsx)

Data for the US: [Google sheets](https://docs.google.com/spreadsheets/d/1pxuTu10uO7MsBaKA554XSuCpnF--FTqwdnl_sUHfWro/edit#gid=265926435), [CSV](google_reports/mobility_report_US.csv), [Excel](google_reports/mobility_report_US.csv)

[**Apple reports**](apple_reports)

## How to run script
```bash
pip install -r requirements.txt
python source.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 

[Place to discuss use cases for this data](https://github.com/ActiveConclusion/COVID19_mobility/issues/4)

## Dashboards based on these data
1. [Dashboard for the US-1](https://public.tableau.com/profile/karl3594#!/vizhome/State-by-StateCOVID-19MobilityChanges/ChangesbyState)
2. [Dashboard for the US-2](https://public.tableau.com/profile/sky.quintin#!/vizhome/Mobilitydata/CommunityMobility)
3. [Dashboard for the world](https://public.tableau.com/profile/ryansoares#!/vizhome/COVID-19CommunityMobility/Dashboard1)
4. [Balefire COVID-19 USA Data Explorer](http://balefire.info/)
5. [Here can be your great dashboard/visualization]

## Articles
1. [Is Your Community Doing Enough To Fight COVID-19?](https://towardsdatascience.com/is-your-community-doing-enough-to-fight-covid-19-aa745b424eb1) by [Molly Liebeskind](https://towardsdatascience.com/@molly.liebeskind)
2. [Here can be your great article/research publication]
