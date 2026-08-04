import logging

from ingestion.database import get_session, init_db
from ingestion.database import record_ingest_run
from ingestion.ingest_crypto import ingest_crypto
from ingestion.ingest_sports import ingest_sports
from ingestion.ingest_weather import ingest_weather

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def main():
    init_db()
    session = get_session()

    summary = {}

    try:
        weather_count = ingest_weather(session)
        record_ingest_run(session, "weather", weather_count)
        summary["weather_records"] = weather_count
        logging.info("Weather ingestion complete: %s records", weather_count)
    except Exception as exc:
        logging.exception("Weather ingestion failed")
        summary["weather_error"] = str(exc)

    try:
        sports_records, sports_events = ingest_sports(session)
        record_ingest_run(session, "sports", sports_records)
        summary["sports_records"] = sports_records
        summary["sports_events"] = sports_events
        logging.info("Sports ingestion complete: %s raw record, %s events", sports_records, sports_events)
    except Exception as exc:
        logging.exception("Sports ingestion failed")
        summary["sports_error"] = str(exc)

    try:
        crypto_records, crypto_entries = ingest_crypto(session)
        record_ingest_run(session, "crypto", crypto_records)
        summary["crypto_records"] = crypto_records
        summary["crypto_entries"] = crypto_entries
        logging.info("Crypto ingestion complete: %s raw record, %s coins", crypto_records, crypto_entries)
    except Exception as exc:
        logging.exception("Crypto ingestion failed")
        summary["crypto_error"] = str(exc)

    try:
        from sqlalchemy import text

        weather_total = session.execute(text("SELECT COUNT(*) FROM raw_weather")).scalar_one()
        sports_total = session.execute(text("SELECT COUNT(*) FROM raw_sports")).scalar_one()
        crypto_total = session.execute(text("SELECT COUNT(*) FROM raw_crypto")).scalar_one()
        logging.info(
            "Database totals after ingestion: weather=%s, sports=%s, crypto=%s",
            weather_total,
            sports_total,
            crypto_total,
        )
        summary["db_totals"] = {
            "raw_weather": weather_total,
            "raw_sports": sports_total,
            "raw_crypto": crypto_total,
        }
    except Exception as exc:
        logging.exception("Failed to fetch database totals")
        summary["totals_error"] = str(exc)

    session.close()
    return summary


if __name__ == "__main__":
    result = main()
    print(result)
