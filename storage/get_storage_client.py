from storage.base import StorageClient
from storage.clickhouse import ClickhouseCredentials, ClickhouseStorageClient


def get_storage_client() -> StorageClient:
    credentials = ClickhouseCredentials(host='localhost', port=9000, database='tickers')
    client = ClickhouseStorageClient(credentials=credentials)
    return client