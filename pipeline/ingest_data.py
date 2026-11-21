#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]


@click.command()
@click.option("--pg-user", default="root", show_default=True, help="PostgreSQL user")
@click.option("--pg-pass", default="root", show_default=True, help="PostgreSQL password")
@click.option("--pg-host", default="localhost", show_default=True, help="PostgreSQL host")
@click.option("--pg-port", default=5433, show_default=True, type=int, help="PostgreSQL port")
@click.option("--pg-db", default="ny_taxi", show_default=True, help="PostgreSQL database name")
@click.option("--year", default=2021, show_default=True, type=int, help="Year of the data to ingest")
@click.option("--month", default=1, show_default=True, type=int, help="Month of the data to ingest")
@click.option("--chunksize", default=100000, show_default=True, type=int, help="Chunk size for reading CSV")
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize):
    """Ingest NYC taxi data into PostgreSQL."""
    url = (
        "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"
        f"yellow/yellow_tripdata_{year:04d}-{month:02d}.csv.gz"
    )

    engine = create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )

    df = pd.read_csv(url, nrows=0, dtype=dtype, parse_dates=parse_dates)
    df.head(n=0).to_sql(name="yellow_taxi_data", con=engine, if_exists="replace")

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )

    for df_chunk in tqdm(df_iter):
        df_chunk.to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="append",
        )

    print(f"Ingested yellow_tripdata_{year:04d}-{month:02d} into {pg_db}.yellow_taxi_data")


if __name__ == "__main__":
    main()
