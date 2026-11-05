"""Run the whole pipeline once without Prefect: extract, load, dbt run, dbt test."""

from dbt.cli.main import dbtRunner

from config import PROJECT_ROOT
from extract import download
from load import load_all

DBT_DIR = PROJECT_ROOT / "dbt"


def run_dbt(command: str):
    """Run a dbt command and stop the pipeline if it fails."""
    result = dbtRunner().invoke(
        [command, "--project-dir", str(DBT_DIR), "--profiles-dir", str(DBT_DIR)]
    )
    if not result.success:
        raise RuntimeError(f"dbt {command} failed")


def main():
    download()
    load_all()
    run_dbt("run")
    run_dbt("test")


if __name__ == "__main__":
    main()