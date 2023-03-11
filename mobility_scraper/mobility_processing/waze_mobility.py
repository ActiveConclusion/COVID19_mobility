import pandas as pd


def build_report(countries_source, cities_source):
    """Build cleaned Waze report (transform dates from string to date format, merge country&city-level data,
    add geo_type column)

    Args:
        countries_source: location of the raw Waze country-level CSV report
        cities_source: location of the raw Waze city-level CSV report

    Returns:
       waze (DataFrame): generated Waze report
    """
    waze_countries = pd.read_csv(countries_source, parse_dates=["Date"])
    waze_cities = pd.read_csv(cities_source, parse_dates=["Date"])
    waze_countries["City"] = "Total"
    waze_countries["geo_type"] = "country"
    waze_cities["geo_type"] = "city"

    waze = waze_countries.append(waze_cities)
    waze = waze.rename(
        columns={
            "Country": "country",
            "City": "city",
            "Date": "date",
            "% Change In Waze Driven Miles/KMs": "driving_waze",
        }
    )
    waze["driving_waze"] = waze["driving_waze"] * 100
    waze["date"] = waze["date"].dt.date
    waze = waze.loc[:, ["country", "city", "geo_type", "date", "driving_waze"]]
    waze = waze.sort_values(by=["country", "city", "geo_type", "date"]).reset_index(
        drop=True
    )
    return waze