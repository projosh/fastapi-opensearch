from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from app.models import LogEntry
from app.opensearch_client import client
from app.utils import create_index_if_not_exists
from datetime import datetime

app = FastAPI()

@app.post("/logs")
def ingest_log(log: LogEntry):
    index_name = f"logs-{log.service}"
    create_index_if_not_exists(client, index_name)
    response = client.index(index=index_name, body=log.dict())
    return {"result": response["result"], "id": response["_id"]}

@app.get("/logs")
def search_logs(
    service: Optional[str] = None,
    level: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
):
    query = {"bool": {"must": []}}

    if service:
        query["bool"]["must"].append({"term": {"service": service}})
    if level:
        query["bool"]["must"].append({"term": {"level": level}})
    if start_time and end_time:
        query["bool"]["must"].append({
            "range": {
                "timestamp": {
                    "gte": start_time.isoformat(),
                    "lte": end_time.isoformat()
                }
            }
        })

    index_pattern = f"logs-{service}" if service else "logs-*"
    response = client.search(index=index_pattern, body={"query": query})
    return {"hits": [hit["_source"] for hit in response["hits"]["hits"]]}
