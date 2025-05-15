"""
Load Yello Taxi Trip Records downloaded by `yello_taxi_trip_internet_to_file` to Postgres

Source files:
    src/yello_taxi_trip/yello_tripdata_<yyyy>_<mm>.parquet
"""

SOURCE_FOLDER = "src/yello_taxi_trip"

from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from airflow.decorators import dag, task

from utils.database import get_postgresql_conn


TMP_TAXI_TRIP_FILE_FOLDER = "src/yello_taxi_trip"

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
}

@dag(
    dag_id="yello_taxi_trip_file_to_postgres",
    default_args=default_args,
    description="Download yello-taxi-trip",
    schedule_interval="* 10 10 * *",
    start_date=datetime(2022, 1, 1),
    catchup=False,
    tags=["staging"]
)
def yello_taxi_trip_file_to_postgres():

    @task
    def e_yellow_taxi_trip_to_df() -> pd.DataFrame:
        """"""

    e_yellow_taxi_trip_to_df()


# Instantiate the DAG
yello_taxi_trip_file_to_postgres()
