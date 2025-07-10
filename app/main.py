from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Optional
from opensearch_client import get_client
from schemas import LogInput, LogOutput
import os

app = FastAPI()

# CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = get_client()

@app.post("/logs", response_model=LogOutput)
def create_log(log: LogInput):
    index = f"logs-{datetime.now().strftime('%Y.%m.%d')}"
    res = client.index(index=index, body=log.dict())
    return {"id": res["_id"], **log.dict()}

@app.get("/logs/search", response_model=List[LogOutput])
def search_logs(q: Optional[str] = None, level: Optional[str] = None, service: Optional[str] = None):
    must = []

    if q:
        must.append({"match": {"message": q}})
    if level:
        must.append({"term": {"level": level}})
    if service:
        must.append({"term": {"service": service}})

    query = {"query": {"bool": {"must": must}}, "sort": [{"timestamp": {"order": "desc"}}]}

    res = client.search(index="logs-*", body=query)
    return [{"id": hit["_id"], **hit["_source"]} for hit in res["hits"]["hits"]]
