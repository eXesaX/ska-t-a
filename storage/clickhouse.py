import os
from dataclasses import dataclass
from datetime import datetime
from pprint import pprint
from typing import Sequence, Iterable

from clickhouse_driver import Client

from storage.base import StorageCredentials, StorageClient, Ticker


@dataclass
class ClickhouseCredentials(StorageCredentials):
    database: str


class ClickhouseStorageClient(StorageClient):
    TICKERS_TABLE_NAME = 'tickers'
    TICKERS_COUNT = 100

    def __init__(self, credentials: StorageCredentials):
        self._host = credentials.host
        self._port = credentials.port
        self._database = credentials.database
        self._client = Client(self._host, self._port)
        self._init_schema()

    def _init_schema(self):
        self._create_database()
        self._create_tables()

    def _create_database(self):
        self._client.execute(f'CREATE DATABASE IF NOT EXISTS {self._database};')

    def _create_tables(self):
        ticker_fields = ",\n".join([f'ticker_{str(i).zfill(2)} Int64' for i in range(self.TICKERS_COUNT)])
        self._client.execute(f'''CREATE TABLE IF NOT EXISTS `{self._database}`.`{self.TICKERS_TABLE_NAME}` (
            timestamp DateTime,
            {ticker_fields}
        ) engine = MergeTree order by (timestamp);''')

    def get_tickers(self, ticker_names: Iterable[str], start: datetime, stop: datetime) -> Iterable[Ticker]:
        field_list = ','.join([f'`{name}`' for name in ticker_names])
        start = start.strftime('%Y-%m-%d %H:%M:%S')
        stop = stop.strftime('%Y-%m-%d %H:%M:%S')
        query = f'''
            SELECT `timestamp`, {field_list} FROM `{self._database}`.`{self.TICKERS_TABLE_NAME}`
            WHERE `timestamp` > '{start}' AND `timestamp` < '{stop}';
        '''
        print(query)
        data = self._client.execute(query)
        result = []
        for row in data:
            timestamp = row[0]
            tickers = row[1:]
            for name, ticker_value in zip(ticker_names, tickers):
                result.append(Ticker(name=name, datetime=timestamp, value=ticker_value))
        return result

    def insert_tickers(self, row: Iterable[int], timestamp: datetime):
        data = [timestamp]
        data.extend(row)
        return self._client.execute(f'INSERT INTO `{self._database}`.`{self.TICKERS_TABLE_NAME}` VALUES', [data])









