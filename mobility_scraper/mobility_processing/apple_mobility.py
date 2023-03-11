import json
import urllib.request

import pandas as pd


def get_link():
    """Get link of Apple Mobility Trends report file

    Returns:
        link (str): link of Apple Mobility Trends report file
    """
    # get link via API
    json_link = "https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v3/index.json"
    with urllib.request.urlopen(json_link) as url:
        json_data = json.loads(url.read().decode())
    link = (
        "https://covid19-static.cdn-apple.com"
        + json_data["basePath"]
        + json_data["regions"]["en-us"]["csvPath"]
    )
    return link


def build_report(
    source,
    report_type="regions",
):
    """Build cleaned Apple report (transform dates from columns to rows, add country names for subregions and cities)
    for the worldwide or for some country (currently only for the US)

     Args:
         source: location of the raw Apple CSV report
         destination: destination file path
         report_type: two options available: "regions" - report for the worldwide, "US" - report for the US

     Returns:
        apple (DataFrame): generated Apple report
    """
    apple = pd.read_csv(source, low_memory=False)
    apple = apple.drop(columns=["alternative_name"])
    apple["country"] = apple.apply(
        lambda x: x["region"] if x["geo_type"] == "country/region" else x["country"],
        axis=1,
    )

    if report_type == "regions":
        apple = apple[apple.geo_type != "county"]
        apple["sub-region"] = apple.apply(
            lambda x: "Total"
            if x["geo_type"] == "country/region"
            else (x["region"] if x["geo_type"] == "sub-region" else x["sub-region"]),
            axis=1,
        )
        apple["subregion_and_city"] = apple.apply(
            lambda x: "Total" if x["geo_type"] == "country/region" else x["region"],
            axis=1,
        )
        apple = apple.drop(columns=["region"])
        apple["sub-region"] = apple["sub-region"].fillna(apple["subregion_and_city"])

        apple = apple.melt(
            id_vars=[
                "geo_type",
                "subregion_and_city",
                "sub-region",
                "transportation_type",
                "country",
            ],
            var_name="date",
        )
        apple["value"] = apple["value"] - 100

        apple = apple.pivot_table(
            index=["geo_type", "subregion_and_city", "sub-region", "date", "country"],
            columns="transportation_type",
        ).reset_index()
        apple.columns = [t + (v if v != "value" else "") for v, t in apple.columns]
        apple = apple.loc[
            :,
            [
                "country",
                "sub-region",
                "subregion_and_city",
                "geo_type",
                "date",
                "driving",
                "transit",
                "walking",
            ],
        ]
        apple = apple.sort_values(
            by=["country", "sub-region", "subregion_and_city", "date"]
        ).reset_index(drop=True)
    elif report_type == "US":
        apple = apple[apple.country == "United States"].drop(columns=["country"])
        apple["sub-region"] = (
            apple["sub-region"]
            .fillna(apple["region"])
            .replace({"United States": "Total"})
        )
        apple["region"] = apple.apply(
            lambda x: x["region"]
            if (x["geo_type"] == "city" or x["geo_type"] == "county")
            else "Total",
            axis=1,
        )
        apple = apple.rename(
            columns={"sub-region": "state", "region": "county_and_city"}
        )

        apple = apple.melt(
            id_vars=["geo_type", "state", "county_and_city", "transportation_type"],
            var_name="date",
        )
        apple["value"] = apple["value"] - 100

        apple = apple.pivot_table(
            index=["geo_type", "state", "county_and_city", "date"],
            columns="transportation_type",
        ).reset_index()
        apple.columns = [t + (v if v != "value" else "") for v, t in apple.columns]

        apple = apple.loc[
            :,
            [
                "state",
                "county_and_city",
                "geo_type",
                "date",
                "driving",
                "transit",
                "walking",
            ],
        ]
        apple = apple.sort_values(
            by=["state", "county_and_city", "geo_type", "date"]
        ).reset_index(drop=True)
    return apple