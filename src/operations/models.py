from sqlalchemy import Table, Integer, Column, String, TIMESTAMP

from src.database import metadata

operation = Table(
    'operation',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('quantity', String),
    Column('figi', String),
    Column('instrument_type', String, nullable=False),
    Column('date', TIMESTAMP),
    Column('type', String),
)