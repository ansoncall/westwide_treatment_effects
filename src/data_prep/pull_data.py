"""Downloads and extracts raw data from online sources."""

import json
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

import geopandas as gpd

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


# TWIG treatment data
TWIG_URL = "https://sweri-treatment-index.s3.us-west-2.amazonaws.com/treatment_index.zip"

zip_path = RAW_DIR / "treatment_index.zip"
urllib.request.urlretrieve(TWIG_URL, zip_path)

with zipfile.ZipFile(zip_path) as zf:
    zf.extractall(RAW_DIR / "treatment_index")


# Wildfire perimeter data (ArcGIS FeatureServer)
# Recent final:   https://data-nifc.opendata.arcgis.com/datasets/nifc::wfigs-interagency-fire-perimeters/about
# Historical:     https://data-nifc.opendata.arcgis.com/datasets/nifc::interagencyfireperimeterhistory-all-years-view/about
# Daily progress: https://nifc.maps.arcgis.com/home/item.html?id=7fa2437e625d49f7af1017c8617b68c1

FIRE_SOURCES = {
    "fire_perimeters_recent": (
        "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Interagency_Perimeters/FeatureServer/0",
        2000,
    ),
    "fire_perimeters_historical": (
        "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/InterAgencyFirePerimeterHistory_All_Years_View/FeatureServer/0",
        2000,
    ),
    "fire_perimeters_daily": (
        "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Daily_Perimeters_Public/FeatureServer/0",
        1000,
    ),
}


def scrape_feature_service(base_url, out_path, page_size):
    count_params = urllib.parse.urlencode({"where": "1=1", "returnCountOnly": "true", "f": "json"})
    total = json.loads(urllib.request.urlopen(f"{base_url}/query?{count_params}").read())["count"]
    print(f"Fetching {total} features...")

    features = []
    offset = 0
    while offset < total:
        params = urllib.parse.urlencode({
            "where": "1=1",
            "outFields": "*",
            "resultOffset": offset,
            "resultRecordCount": page_size,
            "f": "geojson",
        })
        batch = json.loads(urllib.request.urlopen(f"{base_url}/query?{params}").read()).get("features", [])
        features.extend(batch)
        offset += len(batch)
        print(f"  {offset} / {total}")
        if not batch:
            break

    gpd.GeoDataFrame.from_features(features, crs="EPSG:4326").to_file(out_path, driver="GPKG")


for name, (url, page_size) in FIRE_SOURCES.items():
    scrape_feature_service(url, RAW_DIR / f"{name}.gpkg", page_size)