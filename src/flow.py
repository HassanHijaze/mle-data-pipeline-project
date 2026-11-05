"""Prefect flow that runs the Green Taxi ELT pipeline: first 2 minutes after start, then daily."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dbt.cli.main import dbtRunner
from prefect import flow, task
from prefect.schedules import Interval

from config import PROJECT_ROOT
from extract import download
from load import load_all

DBT_DIR = PROJECT_ROOT / "dbt"


@task(retries=3, retry_delay_seconds=10)
def extract():
    """Download the monthly files; retry because the network can fail."""
    download()


@task(retries=2, retry_delay_seconds=5)
def load():
    """Load the staged files into Postgres; retry in case the database isn't ready."""
    load_all()


@task
def run_dbt(command: str):
    """Run a dbt command (run or test) and fail the task if dbt fails."""
    result = dbtRunner().invoke(
        [command, "--project-dir", str(DBT_DIR), "--profiles-dir", str(DBT_DIR)]
    )
    if not result.success:
        raise RuntimeError(f"dbt {command} failed")


@flow(name="green-taxi-elt")
def green_taxi_pipeline():
    extract()
    load()
    run_dbt("run")
    run_dbt("test")


if __name__ == "__main__":
    # First run 2 minutes from now, then every day at the same time
    start = datetime.now(ZoneInfo("Europe/Berlin")) + timedelta(minutes=2)

    green_taxi_pipeline.serve(
        name="green-taxi-elt-deployment",
        schedule=Interval(timedelta(days=1), anchor_date=start, timezone="Europe/Berlin"),
    )