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
