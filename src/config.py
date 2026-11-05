"""Central settings for the Green Taxi pipeline."""

from pathlib import Path

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]
STAGING_DIR = PROJECT_ROOT / "data" / "staging"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"

# Download settings
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
TAXI_TYPE = "green"
YEAR = 2025
MONTHS = [1, 2, 3]

# Database settings
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "green_taxi"
RAW_TABLE = "green_taxi"
