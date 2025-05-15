with pu_location_id as (
    select distinct("PULocationID") as location_id from {{ source('src', 'yello_taxi_trip_records') }}
),
do_location_id as (
    select distinct("DOLocationID") as location_id from {{ source('src', 'yello_taxi_trip_records') }}
)

select distinct location_id from (
	select location_id from pu_location_id
	union
	select location_id from do_location_id
)
