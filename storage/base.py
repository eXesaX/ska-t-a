from dataclasses import dataclass
from datetime import datetime
from typing import Sequence, Iterable


@dataclass
class StorageCredentials:
    host: str
    port: int
    database: str


@dataclass
class Ticker:
    name: str
    datetime: datetime
    value: int


class StorageClient:
    def __init__(self, credentials: StorageCredentials, *args, **kwargs):
        raise NotImplemented()

    def get_tickers(self, ticker_names: Iterable[str], start: datetime, stop: datetime) -> Iterable[Ticker]:
        """Get ticker values by name list in given time period"""
        raise NotImplemented()

    def insert_tickers(self, row: Iterable[int], timestamp: datetime):
        """Insert ticker row"""
        raise NotImplemented()
