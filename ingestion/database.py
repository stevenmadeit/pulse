import json
import os
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get(
    "PULSE_DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres123@localhost:5432/pulse",
)

engine = create_engine(DATABASE_URL, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


class RawWeather(Base):
    __tablename__ = "raw_weather"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(128), nullable=False)
    raw_json = Column(Text, nullable=False)
    ingested_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class RawSports(Base):
    __tablename__ = "raw_sports"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(128), nullable=False)
    raw_json = Column(Text, nullable=False)
    ingested_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class RawCrypto(Base):
    __tablename__ = "raw_crypto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(128), nullable=False)
    raw_json = Column(Text, nullable=False)
    ingested_at = Column(DateTime, nullable=False, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(engine)


def get_session():
    return SessionLocal()


def save_raw_record(session, model, source, raw_data):
    record = model(source=source, raw_json=json.dumps(raw_data), ingested_at=datetime.utcnow())
    session.add(record)
    return record


class RawIngestRun(Base):
    __tablename__ = "raw_ingest_runs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(64), nullable=False)
    record_count = Column(Integer, nullable=False)
    run_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(64), nullable=False)
    check_type = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(16), nullable=False)
    status = Column(String(32), nullable=False, default="open")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    ai_summary = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)


def record_ingest_run(session, source: str, record_count: int):
    run = RawIngestRun(source=source, record_count=record_count, run_at=datetime.utcnow())
    session.add(run)
    session.commit()
    return run


def create_incident(session, source: str, check_type: str, description: str, severity: str = "low"):
    incident = Incident(
        source=source,
        check_type=check_type,
        description=description,
        severity=severity,
        status="open",
        created_at=datetime.utcnow(),
    )
    session.add(incident)
    session.commit()
    return incident
