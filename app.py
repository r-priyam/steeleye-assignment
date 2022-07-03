from typing import List

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_scan
from fastapi import FastAPI, HTTPException

from config import config
from schema import Trade

app = FastAPI()
es = AsyncElasticsearch(
    cloud_id=config.elastic_cloud_id,
    http_auth=(config.elastic_user, config.elastic_password),
)


@app.on_event("shutdown")
async def app_shutdown():
    await es.close()


@app.get("/trades", response_model=List[Trade])
async def list_trades():
    return [
        x["_source"]
        async for x in async_scan(
            es,
            index="steeleye",
        )
    ]


@app.get(
    "/trade/{trade_id}",
    response_model=Trade,
    responses={
        404: {"description": "Trade not found"},
    },
)
async def single_trade(trade_id: str):
    result = await es.search(index="steeleye", query={"match": {"trade_id": trade_id}})

    if not result["hits"]["hits"]:
        raise HTTPException(404, "Trade not found")

    return result["hits"]["hits"][0]["_source"]


@app.get(
    "/search-trades/{value}",
    response_model=Trade,
    responses={
        404: {"description": "Trade not found"},
    },
)
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

    if not result["hits"]["hits"]:
        raise HTTPException(404, "Trade not found")

    return result["hits"]["hits"][0]["_source"]


@app.get("")
async def filter_trades():
    ...
