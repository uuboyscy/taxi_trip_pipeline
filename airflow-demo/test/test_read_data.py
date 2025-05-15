import pandas as pd

file_path = "tmp/taxi_trip/yellow_tripdata_2022-01.parquet"

df = pd.read_parquet(file_path)

print(df)