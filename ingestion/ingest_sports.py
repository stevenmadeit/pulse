import requests

from ingestion.database import RawSports, save_raw_record

ESPN_NFL_SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"


def ingest_sports(session):
    response = requests.get(ESPN_NFL_SCOREBOARD, timeout=20)
    response.raise_for_status()
    payload = response.json()
    payload["source"] = "espn-nfl"
    payload["fetched_at"] = response.headers.get("Date")

    save_raw_record(session, RawSports, "espn-nfl", payload)
    session.commit()
    event_count = len(payload.get("events", []))
    return 1, event_count
