import os
import shutil
import subprocess
from pathlib import Path

from dagster import AssetExecutionContext, Definitions, ScheduleDefinition, asset, define_asset_job

ROOT_DIR = Path(__file__).resolve().parent
DBT_DIR = ROOT_DIR / "transform"
DBT_EXECUTABLE = ROOT_DIR / "dbt_venv" / "Scripts" / "dbt.exe"


def _get_dbt_executable() -> str:
    if DBT_EXECUTABLE.exists():
        return str(DBT_EXECUTABLE)

    resolved = shutil.which("dbt")
    if resolved:
        return resolved

    raise FileNotFoundError("dbt executable was not found; expected dbt_venv/Scripts/dbt.exe")


@asset
def initialize_database(context: AssetExecutionContext):
    from ingestion.database import init_db

    init_db()
    context.add_output_metadata({"status": "database initialized"})
    return "database initialized"


@asset(deps=[initialize_database])
def ingest_weather(context: AssetExecutionContext):
    from ingestion.database import get_session
    from ingestion.ingest_weather import ingest_weather as run_ingest_weather

    session = get_session()
    try:
        count = run_ingest_weather(session)
        context.add_output_metadata({"weather_records": count})
        return count
    finally:
        session.close()


@asset(deps=[initialize_database])
def ingest_sports(context: AssetExecutionContext):
    from ingestion.database import get_session
    from ingestion.ingest_sports import ingest_sports as run_ingest_sports

    session = get_session()
    try:
        records, events = run_ingest_sports(session)
        context.add_output_metadata({"sports_records": records, "sports_events": events})
        return {"records": records, "events": events}
    finally:
        session.close()


@asset(deps=[initialize_database])
def ingest_crypto(context: AssetExecutionContext):
    from ingestion.database import get_session
    from ingestion.ingest_crypto import ingest_crypto as run_ingest_crypto

    session = get_session()
    try:
        records, coins = run_ingest_crypto(session)
        context.add_output_metadata({"crypto_records": records, "crypto_coins": coins})
        return {"records": records, "coins": coins}
    finally:
        session.close()


@asset(deps=[ingest_weather, ingest_sports, ingest_crypto])
def run_dbt_build(context: AssetExecutionContext):
    dbt_executable = _get_dbt_executable()
    env = os.environ.copy()
    env.setdefault("PULSE_DATABASE_URL", "postgresql+psycopg2://postgres:postgres123@localhost:5432/pulse")

    result = subprocess.run(
        [dbt_executable, "build", "--profiles-dir", str(DBT_DIR), "--project-dir", str(DBT_DIR)],
        cwd=ROOT_DIR,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    context.add_output_metadata({"dbt_stdout": result.stdout, "dbt_stderr": result.stderr})
    return result.stdout


pulse_pipeline = define_asset_job(
    name="pulse_pipeline",
    selection=[ingest_weather, ingest_sports, ingest_crypto, run_dbt_build],
)

hourly_schedule = ScheduleDefinition(
    job=pulse_pipeline,
    cron_schedule="0 * * * *",
    execution_timezone="UTC",
)


defs = Definitions(
    assets=[initialize_database, ingest_weather, ingest_sports, ingest_crypto, run_dbt_build],
    jobs=[pulse_pipeline],
    schedules=[hourly_schedule],
)
