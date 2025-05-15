"""
Download Yellow Taxi Trip Records from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Source files URL pattern:
    https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_<yyyy>-<mm>.parquet
"""

from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import requests
from airflow.decorators import dag, task


YELLO_TAXI_TRIP_RECORDS_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-%02d.parquet"
TMP_TAXI_TRIP_FILE_FOLDER = "tmp/yello_taxi_trip/"
TARGET_FOLDER = "src/yello_taxi_trip"

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
}

@dag(
    dag_id="download_yello_taxi_trip_to_postgres",
    default_args=default_args,
    description="Download yello-taxi-trip",
    schedule_interval="* 10 10 * *",
    start_date=datetime(2022, 1, 1),
    catchup=False,
    tags=["source"]  # Optional: Add tags for better filtering in the UI
)
def download_yello_taxi_trip_to_postgres():
    @task
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

            print(str(taxi_trip_file_path), "Downloaded")
            download_path_list.append(taxi_trip_file_path)

        return download_path_list
    
    @task
    def check_data_quality(download_path_list: list[str]) -> None:
        """Check data quality and move operated files into src folder."""
        Path(TARGET_FOLDER).mkdir(parents=True, exist_ok=True)
        for download_path in download_path_list:
            print(f"Reading {download_path}")
            df = pd.read_parquet(download_path)

            ### Quality check ###
            ### Quality check ###

            df.to_parquet(Path(TARGET_FOLDER) / download_path.name)


    download_path_list = download_yello_taxi_trip_to_file()
    check_data_quality(download_path_list)


# Instantiate the DAG
download_yello_taxi_trip_to_postgres()
