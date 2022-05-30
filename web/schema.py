from typing import List, Iterable
from datetime import datetime

from pydantic import BaseModel

from storage.base import Ticker


class TickerDatapoint(BaseModel):
    timestamp: float
    value: int


class TickerResponse(BaseModel):
    points: List[TickerDatapoint]


def make_ticker_response(tickers: Iterable[Ticker]) -> TickerResponse:
    # print(tickers)
    datapoints = [TickerDatapoint(timestamp=ticker.datetime.timestamp(), value=ticker.value) for ticker in tickers]
    # print(datapoints)
    return TickerResponse(points=datapoints)