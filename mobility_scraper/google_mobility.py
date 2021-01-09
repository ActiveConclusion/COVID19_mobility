from pathlib import Path

import pandas as pd


def build_report(source,
    report_type="regions",
    countries=None,
    world_regions=None,
    country_regions_file=None,
):
    """Build cleaned Google report for the worldwide

    Args:
        source: location of the raw Google CSV report
        report_type: available options:
                        1) "regions" - basic report for the worldwide
                        2) "US" - report for the US
                        3) "regions_detailed" - detailed report for selected countries
                        4) "world_regions_detailed" - detailed report for selected regions (Europe, Asia etc)
        countries: list of countries for "regions_detailed" option. If None - all countries selected
        world_regions: list of regions for "world_regions_detailed option. If None - all regions selected
        country_regions_file: path of the CSV file with matching table of countries and regions

    Returns:
       google (DataFrame): generated Google report
    """
    # read the raw report
    google = pd.read_csv(source, low_memory=False)
    # shorten value column names
    google.columns = google.columns.str.replace(r"_percent_change_from_baseline", "")
    # remove underscores from column names
    google.columns = google.columns.str.replace(r"_", " ")
    # rename country column
    google = google.rename(columns={"country region": "country"})
    if report_type == "regions":
        # remove data of subregions of the second level
        google = google[google["sub region 2"].isnull()]
        # remove metropolitan data
        google = google[google["metro area"].isnull()]
        # rename region column
        google = google.rename(columns={"sub region 1": "region"})
        google = google.loc[
            :,
            [
                "country",
                "region",
                "date",
                "retail and recreation",
                "grocery and pharmacy",
                "parks",
                "transit stations",
                "workplaces",
                "residential",
            ],
        ]
        google["region"].fillna("Total", inplace=True)
    elif report_type == "US":
        google = google[(google["country"] == "United States")]
        google = google.rename(
            columns={"sub region 1": "state", "sub region 2": "county"}
        )
        google = google.loc[
            :,
            [
                "state",
                "county",
                "date",
                "retail and recreation",
                "grocery and pharmacy",
                "parks",
                "transit stations",
                "workplaces",
                "residential",
            ],
        ]
        google["state"].fillna("Total", inplace=True)
        google["county"].fillna("Total", inplace=True)
    elif report_type == "regions_detailed" or report_type == "world_regions_detailed":
        if countries is not None and report_type == "regions_detailed":
            google = google[google.country.isin(countries)]
        if report_type == "world_regions_detailed":
            if Path(country_regions_file).is_file():
                country_regions = pd.read_csv(country_regions_file)
            google = pd.merge(google, country_regions, on="country")
            if world_regions is not None:
                google = google[google.world_region.isin(world_regions)]
        # metro area -> sub region 1
        google["sub region 1"] = google.apply(
            lambda x: x["sub region 1"]
            if isinstance(x["sub region 1"], str)
            else x["metro area"],
            axis=1,
        )
        column_list = (
            ["world_region"] if report_type == "world_regions_detailed" else []
        )
        column_list = column_list + [
            "country",
            "sub region 1",
            "sub region 2",
            "date",
            "retail and recreation",
            "grocery and pharmacy",
            "parks",
            "transit stations",
            "workplaces",
            "residential",
        ]
        google = google.loc[:, column_list]
        google["sub region 1"].fillna("Total", inplace=True)
        google["sub region 2"].fillna("Total", inplace=True)
    return google