from pathlib import Path
import requests
import pandas as pd

YELLO_TAXI_TRIP_RECORDS_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-%02d.parquet"
TMP_TAXI_TRIP_FILE_FOLDER = "tmp/taxi_trip/"

def download_yello_taxi_trip_to_file() -> list[str]:
    Path(TMP_TAXI_TRIP_FILE_FOLDER).mkdir(parents=True, exist_ok=True)

    download_path_list = []
    for month_number in range(12):
        specific_month_taxi_trip_url = YELLO_TAXI_TRIP_RECORDS_URL % (month_number + 1)
        taxi_trip_file_name = specific_month_taxi_trip_url.split("/")[-1]
        taxi_trip_file_path = Path(TMP_TAXI_TRIP_FILE_FOLDER) / taxi_trip_file_name

        taxi_trip_parquet_content = requests.get(specific_month_taxi_trip_url).content
        with taxi_trip_file_path.open("wb") as f:
            f.write(taxi_trip_parquet_content)

        download_path_list.append(taxi_trip_file_path)

    return download_path_list

download_yello_taxi_trip_to_file()