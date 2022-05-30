import asyncio
from datetime import datetime, timedelta
from time import sleep
from typing import Tuple, Iterable

from feed.generator import generate_movement
from pubsub.get_pubsub_client import get_pubsub_client
from storage.get_storage_client import get_storage_client

TICKERS_COUNT = 100
TICKERS_TOPIC_NAME = 'tickers'


def get_ticker_data() -> Tuple[Iterable[int], datetime]:
    timestamp = datetime.now()
    tickers = [generate_movement() for i in range(TICKERS_COUNT)]
    yield tickers, timestamp
    sleep(1)


async def main():
    storage = get_storage_client()
    pubsub = get_pubsub_client()
    while True:
        for tickers, timestamp in get_ticker_data():
            print(storage.insert_tickers(tickers, timestamp))
            await pubsub.publish(TICKERS_TOPIC_NAME, {'timestamp': timestamp.timestamp(), 'tickers': tickers})


if __name__ == '__main__':
    asyncio.run(main())


