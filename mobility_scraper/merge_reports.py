from pathlib import Path
import pandas as pd


def build_summary_report(
    apple_source,
    google_source,
    country_AtoG_file,
    subregions_AtoG_file,
    report_type="regions",
):
    """Build a merged report from Google and Apple data

    Args:
        apple_source: location of the generated Apple report in CSV
        google_source: location of the generated Google report in CSV
        country_AtoG_file: location of Apple and Google country names matching table in CSV
        subregions_AtoG_file: location of Apple and Google subregions names matching table in CSV
        report_type: two options available: "regions" - report for the worldwide, "US" - report for the US

    Returns:
        summary (DataFrame): merged report from Google and Apple data
    """
    apple = pd.read_csv(apple_source, low_memory=False)
    google = pd.read_csv(google_source, low_memory=False)
    summary = pd.DataFrame()
    # build report for regions
    if report_type == "regions":
        apple = apple.rename(columns={"subregion_and_city": "region"})
        apple = apple.loc[
            :, ["country", "region", "date", "driving", "transit", "walking"]
        ]
        # convert Apple country and sub-region names as in Google
        if country_AtoG_file.is_file():
            country_AtoG = pd.read_csv(country_AtoG_file, index_col=0)
        else:
            country_AtoG = None
        if subregions_AtoG_file.is_file():
            subregions_AtoG = pd.read_csv(subregions_AtoG_file, index_col=0)
        else:
            subregions_AtoG = None
        # convert Apple countries and subregions to Google names
        apple["country"] = apple.apply(
            lambda x: country_AtoG.loc[x["country"], "country_google"]
            if (country_AtoG is not None and x["country"] in country_AtoG.index)
            else x["country"],
            axis=1,
        )
        apple["region"] = apple.apply(
            lambda x: subregions_AtoG.loc[x["region"], "subregion_Google"]
            if (subregions_AtoG is not None and x["region"] in subregions_AtoG.index)
            else x["region"],
            axis=1,
        )
        # merge reports
        apple = apple.set_index(["country", "region", "date"])
        google = google.set_index(["country", "region", "date"])
        summary = google.join(apple, how="outer")
        summary = summary.reset_index(level=["country", "region", "date"])
    elif report_type == "US":
        apple = apple.loc[
            :, ["state", "county_and_city", "date", "driving", "transit", "walking"]
        ]
        apple.loc[apple.state == "Washington DC", "state"] = "District of Columbia"
        apple.loc[apple.county_and_city == "Washington DC", "county_and_city"] = "Total"

        google = google.rename(columns={"county": "county_and_city"})
        # merge reports
        apple = apple.set_index(["state", "county_and_city", "date"])
        google = google.set_index(["state", "county_and_city", "date"])
        summary = google.join(apple, how="outer")
        summary = summary.reset_index(level=["state", "county_and_city", "date"])
    return summary