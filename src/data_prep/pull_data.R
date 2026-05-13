# systematically queries online data sources and compiles raw data
# load packages ----------------------------------------------------------------
library(tidyverse)
library(curl)

# pull TWIG treatment data -----------------------------------------------------
# download zip file
twig_url <-
  "https://sweri-treatment-index.s3.us-west-2.amazonaws.com/treatment_index.zip"
curl_download(twig_url, destfile = "data/raw/treatment_index.zip")
# unzip file
unzip("data/raw/treatment_index.zip", exdir = "data/raw/treatment_index")

# pull current wildfire perimeter data -----------------------------------------

# pull recent wildfire perimeter data ------------------------------------------
# TODO stream this instead of manually downloading and unzipping
# unzip
unzip(
  "data/raw/WFIGS_Interagency_Perimeters_2669477625335384459.zip",
  exdir = "data/raw/recent_wildfire_perimeters"
)

# pull historical wildfire perimeter data --------------------------------------
# TODO stream this instead of manually downloading and unzipping
# unzip
unzip(
  "data/raw/InterAgencyFirePerimeterHistory_All_Years_View_4308794252235299382.zip",
  exdir = "data/raw/historical_wildfire_perimeters"
)

# pull weather data ------------------------------------------------------------
