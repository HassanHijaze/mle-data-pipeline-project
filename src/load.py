"""Load the staged Green Taxi Parquet files into Postgres as one raw table."""

import pandas as pd
from sqlalchemy import create_engine, text

from config import (
    DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER,
    RAW_TABLE, STAGING_DIR,
)


def load_all():
    engine = create_engine(
        f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    files = sorted(STAGING_DIR.glob("green_tripdata_*.parquet"))
    if not files:
        raise FileNotFoundError(f"No files found in {STAGING_DIR}")

    # Drop the old raw table and the dbt views that depend on it; dbt rebuilds them
    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {RAW_TABLE} CASCADE"))

    total_rows = 0
    for file in files:
        df = pd.read_parquet(file)
        df["source_file"] = file.name

        df.to_sql(RAW_TABLE, engine, if_exists="append", index=False, chunksize=10_000)

        total_rows += len(df)
        print(f"Loaded {file.name}: {len(df)} rows")

    print(f"Total rows loaded: {total_rows}")


if __name__ == "__main__":
    load_all()