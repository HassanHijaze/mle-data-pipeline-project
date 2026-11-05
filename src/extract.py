"""Download the monthly Green Taxi Parquet files into the staging folder."""

import requests

from config import BASE_URL, MONTHS, STAGING_DIR, TAXI_TYPE, YEAR


def download():
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    for month in MONTHS:
        file_name = f"{TAXI_TYPE}_tripdata_{YEAR}-{month:02d}.parquet"
        target = STAGING_DIR / file_name

        if target.exists():
            print(f"Skipping {file_name}")
            continue

        response = requests.get(f"{BASE_URL}/{file_name}", timeout=120)
        response.raise_for_status()
        target.write_bytes(response.content)
        print(f"Saved {file_name}")


if __name__ == "__main__":
    download()