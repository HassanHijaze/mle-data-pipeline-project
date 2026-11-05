# Green Taxi Revenue Pipeline

An ELT pipeline that calculates daily revenue from NYC Green Taxi trips for January to March 2025.

```
extract → load into Postgres → dbt models → dbt tests
```

1. **Extract:** `src/extract.py` downloads the three monthly Parquet files into `data/staging/`.
2. **Load:** `src/load.py` loads the raw rows unchanged into the Postgres table `public.green_taxi`.
3. **Transform:** dbt cleans the trips and sums revenue per day in three layers: staging, intermediate and mart.
4. **Test:** dbt checks that the results have no missing values, no duplicate days and no amounts of 0 or less.

You can run the pipeline once with `src/pipeline.py`, or on a schedule with Prefect in `src/flow.py`.

## Project structure

| Path | Description |
| --- | --- |
| `src/config.py` | Download URL, months, folders and database settings |
| `src/extract.py` | Downloads the files, skipping ones that already exist |
| `src/load.py` | Loads the files into Postgres |
| `src/pipeline.py` | Runs the whole pipeline once, without Prefect |
| `src/flow.py` | Prefect flow with retries and a daily schedule |
| `dbt/` | dbt models, tests and the database connection (`profiles.yml`) |
| `notebooks/exploration.ipynb` | Data exploration |

## How to run it

Run all commands from the project root.

**1. Install the dependencies**

```bash
uv sync --all-packages
```

**2. Start Postgres**

```bash
docker run -d --name green-taxi-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=green_taxi -p 5432:5432 postgres:17
```

**3. Run the pipeline once**

```bash
uv run python src/pipeline.py
```

This runs extract, load, `dbt run` and `dbt test` in order. The result is in the table `dbt_dev_mart.fct_daily_revenue`.

**4. Or schedule it with Prefect**

Start the Prefect server in Docker (UI at http://127.0.0.1:4200):

```bash
docker run -d --name prefect-server -p 4200:4200 prefecthq/prefect:3-latest prefect server start --host 0.0.0.0
```

Then serve the flow:

```bash
uv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
uv run python src/flow.py
```

The first run starts 2 minutes later, then the pipeline runs every day at the same time (Berlin time). Keep this terminal open; runs only happen while it's running.

## Cleaning

The staging model keeps only:

- trips picked up from 2025-01-01 to 2025-03-31, since a few trips in the files have dates outside this period;
- trips with `total_amount > 0`, since negative amounts are refunds or voids and zero amounts aren't revenue.

| Stage | Rows |
| --- | ---: |
| Raw | 146,486 |
| Clean | 145,743 |
| Days in the output | 90 |

## Review questions

**1. What steps did you take?**

I explored one month in a notebook, wrote the download script, loaded the raw files into Postgres, built the dbt models and tests, and orchestrated everything with Prefect.

**2. What challenges did you face?**

The first challenge was the data itself. Some trips had dates outside January to March, and some had negative or zero amounts, so I had to decide which trips really count as revenue.

The second was the tools. Getting Docker, Postgres, dbt and Prefect to work together took the most time. For example, Prefect's scheduler didn't work with the SQLAlchemy version dbt needs, so I ran the Prefect server in Docker instead.

**3. What would you do differently with more time?**

I would load only new months instead of reloading everything on each run, and add unit tests for the Python code. I would also start Postgres and Prefect with one Docker Compose file, so the setup takes a single command.