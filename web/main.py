from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocket

from pubsub.get_pubsub_client import get_pubsub_client
from storage.get_storage_client import get_storage_client
from web.schema import TickerResponse, make_ticker_response
from web.websocket import WebsocketConnectionManager

app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")
storage = get_storage_client()
pubsub = get_pubsub_client()


@app.get("/")
async def root(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/ticker", response_model=TickerResponse)
async def ticker(name: str, start: float, stop: float):
    data = storage.get_tickers([name], datetime.fromtimestamp(start), datetime.fromtimestamp(stop))
    return make_ticker_response(data)


TICKERS_NUM = 100


@app.get("/options")
async def options():
    return HTMLResponse('\n'.join([
        f'<option value="ticker_{str(i).zfill(2)}">Ticker {str(i).zfill(2)}</option>'
        for i in range(TICKERS_NUM)
    ]))


websocket_manager = WebsocketConnectionManager()

TICKERS_TOPIC_NAME = 'tickers'


@app.websocket("/ws/{ticker_name}")
async def websocket_endpoint(websocket: WebSocket, ticker_name: str):
    await websocket_manager.connect(websocket, ticker_name)
    await pubsub.subscribe(TICKERS_TOPIC_NAME)

    async for data in pubsub.listen():
        for ticker_num, ticker_value in enumerate(data['tickers']):
            await websocket_manager.broadcast_ticker_value(
                f'ticker_{str(ticker_num).zfill(2)}', ticker_value, data['timestamp'])


