from ingestion.database import init_db, get_session, save_raw_record, RawCrypto, record_ingest_run
from ingestion.quality_checks import run_checks_for_source
import json

if __name__ == '__main__':
    init_db()
    session = get_session()
    # Insert a broken crypto raw record (missing prices)
    broken = {"requested_coins": ["bitcoin"], "bitcoin": {}}
    rec = save_raw_record(session, RawCrypto, "coingecko", broken)
    session.commit()
    # record ingest run count as 1
    record_ingest_run(session, "crypto", 1)
    # run checks
    incs = run_checks_for_source(session, "crypto")
    print('Created incidents:')
    for i in incs:
        print(i.id, i.check_type, i.description, i.severity)
    session.close()
