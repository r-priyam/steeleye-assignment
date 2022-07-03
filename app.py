from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_scan
from fastapi import FastAPI

from config import config

app = FastAPI()
es = AsyncElasticsearch(
    cloud_id=config.elastic_cloud_id,
    http_auth=(config.elastic_user, config.elastic_password),
)


@app.on_event("shutdown")
async def app_shutdown():
    await es.close()


@app.get("/trades")
async def list_trades():
    return [x async for x in async_scan(es, index="steeleye")]


@app.get("/trade/{trade_id}")
async def single_trade(trade_id: str):
    result = await es.search(index="steeleye", query={"match": {"trade_id": trade_id}})
    return result["hits"]["hits"]


@app.get("/search-trades/{value}")
async def search_trades(value: str):
    result = await es.search(
        index="steeleye",
        query={
            "multi_match": {
                "query": value,
                "fields": [
                    "counterparty",
                    "instrument_id",
                    "instrument_name",
                    "trader",
                ],
            }
        },
    )
    return result


@app.get("")
async def filter_trades():
    ...
