from pathlib import Path

# URLs
GOOGLE_URL = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"
WAZE_URLS = (
    "https://raw.githubusercontent.com/ActiveConclusion/waze_mobility_scraper/master/Waze_Country-Level_Data.csv",
    "https://raw.githubusercontent.com/ActiveConclusion/waze_mobility_scraper/master/Waze_City-Level_Data.csv",
)
# Directories
GOOGLE_DIR = "google_reports"
APPLE_DIR = "apple_reports"
WAZE_DIR = "waze_reports"
TOMTOM_DIR = "tomtom_reports"
SUMMARY_DIR = "summary_reports"
# raw file names
GOOGLE_RAW_FILE = "Global_Mobility_Report.csv"
APPLE_RAW_FILE = "applemobilitytrends.csv"
WAZE_RAW_FILES = ("Waze_Country-Level_Data.csv", "Waze_City-Level_Data.csv")
# extensions
EXTENSIONS = (".csv", ".xlsx")
# Google paths
GOOGLE_RAW_ZIP_FILE = "Global_Mobility_Report.zip"
GOOGLE_ZIP_PATH = Path(GOOGLE_DIR, GOOGLE_RAW_ZIP_FILE)
GOOGLE_CSV_PATH = Path(GOOGLE_DIR, GOOGLE_RAW_FILE)

GOOGLE_REGIONS_FILE = "mobility_report_countries"
GOOGLE_US_FILE = "mobility_report_US"
GOOGLE_BRAZIL_FILE = "mobility_report_brazil"
GOOGLE_EUROPE_FILE = "mobility_report_europe"
GOOGLE_ASIA_AFRICA_FILE = "mobility_report_asia_africa"
GOOGLE_AMERICA_OCEANIA_FILE = "mobility_report_america_oceania"

GOOGLE_REGIONS_PATHS = {
    ext: Path(GOOGLE_DIR, GOOGLE_REGIONS_FILE).with_suffix(ext) for ext in EXTENSIONS
}
GOOGLE_US_PATHS = {
    ext: Path(GOOGLE_DIR, GOOGLE_US_FILE).with_suffix(ext) for ext in EXTENSIONS
}
GOOGLE_BRAZIL_PATHS = {
    ext: Path(GOOGLE_DIR, GOOGLE_BRAZIL_FILE).with_suffix(ext) for ext in EXTENSIONS
}
GOOGLE_EUROPE_PATHS = {
    ext: Path(GOOGLE_DIR, GOOGLE_EUROPE_FILE).with_suffix(ext) for ext in EXTENSIONS
}
GOOGLE_ASIA_AFRICA_PATHS = {
    ext: Path(GOOGLE_DIR, GOOGLE_ASIA_AFRICA_FILE).with_suffix(ext)
    for ext in EXTENSIONS
}
GOOGLE_AMERICA_OCEANIA_PATHS = {
    ext: Path(GOOGLE_DIR, GOOGLE_AMERICA_OCEANIA_FILE).with_suffix(ext)
    for ext in EXTENSIONS
}
# Apple paths
APPLE_CSV_PATH = Path(APPLE_DIR, APPLE_RAW_FILE)
APPLE_WORLD_FILE = "apple_mobility_report"
APPLE_US_FILE = "apple_mobility_report_US"

APPLE_WORLD_PATHS = {
    ext: Path(APPLE_DIR, APPLE_WORLD_FILE).with_suffix(ext) for ext in EXTENSIONS
}
APPLE_US_PATHS = {
    ext: Path(APPLE_DIR, APPLE_US_FILE).with_suffix(ext) for ext in EXTENSIONS
}
# Waze paths
WAZE_COUNTRY_LEVEL_PATH = Path(WAZE_DIR, WAZE_RAW_FILES[0])
WAZE_CITY_LEVEL_PATH = Path(WAZE_DIR, WAZE_RAW_FILES[1])
WAZE_REPORT_FILE = "waze_mobility"

WAZE_REPORT_PATHS = {
    ext: Path(WAZE_DIR, WAZE_REPORT_FILE).with_suffix(ext) for ext in EXTENSIONS
}
# TomTom paths
TOMTOM_REPORT_FILE = "tomtom_trafic_index"
TOMTOM_REPORT_PATHS = {
    ext: Path(TOMTOM_DIR, TOMTOM_REPORT_FILE).with_suffix(ext) for ext in EXTENSIONS
}
# Merged reports
SUMMARY_REGIONS_FILE = "summary_report_regions"
SUMMARY_US_FILE = "summary_report_US"
SUMMARY_COUNTRIES_FILE = "summary_report_countries"

SUMMARY_REGIONS_PATHS = {
    ext: Path(SUMMARY_DIR, SUMMARY_REGIONS_FILE).with_suffix(ext) for ext in EXTENSIONS
}
SUMMARY_US_PATHS = {
    ext: Path(SUMMARY_DIR, SUMMARY_US_FILE).with_suffix(ext) for ext in EXTENSIONS
}
SUMMARY_COUNTRIES_PATHS = {
    ext: Path(SUMMARY_DIR, SUMMARY_COUNTRIES_FILE).with_suffix(ext)
    for ext in EXTENSIONS
}

# Auxiliary data paths
AUXILIARY_DIR = "auxiliary_data"
COUNTRY_WORLD_REGIONS_FILE = "country_worldregions.csv"
COUNTRY_APPLE_TO_GOOGLE_FILE = "country_Apple_to_Google.csv"
SUBREGIONS_APPLE_TO_GOOGLE_FILE = "subregions_Apple_to_Google.csv"
COUNTRY_ALPHA_CODES_FILE = "country_alpha_codes.csv"

COUNTRY_WORLD_REGIONS_PATH = Path(AUXILIARY_DIR, COUNTRY_WORLD_REGIONS_FILE)
COUNTRY_APPLE_TO_GOOGLE_PATH = Path(AUXILIARY_DIR, COUNTRY_APPLE_TO_GOOGLE_FILE)
SUBREGIONS_APPLE_TO_GOOGLE_PATH = Path(AUXILIARY_DIR, SUBREGIONS_APPLE_TO_GOOGLE_FILE)
COUNTRY_ALPHA_CODES_PATH = Path(AUXILIARY_DIR, COUNTRY_ALPHA_CODES_FILE)
