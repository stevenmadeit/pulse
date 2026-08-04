import requests

from ingestion.database import RawCrypto, save_raw_record

COINGECKO_SIMPLE_PRICE = "https://api.coingecko.com/api/v3/simple/price"
COINS = [
    "bitcoin",
    "ethereum",
    "binancecoin",
    "ripple",
    "cardano",
    "dogecoin",
    "solana",
    "polkadot",
    "tron",
    "usd-coin",
]


def ingest_crypto(session):
    params = {
        "ids": ",".join(COINS),
        "vs_currencies": "usd",
    }
    response = requests.get(COINGECKO_SIMPLE_PRICE, params=params, timeout=20)
    response.raise_for_status()
    payload = response.json()
    payload["requested_coins"] = COINS

    save_raw_record(session, RawCrypto, "coingecko", payload)
    session.commit()
    return 1, len(payload)
