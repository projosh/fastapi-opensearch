# app/main.py
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from datetime import date
from app import opensearch_client
from app.models import LogEntry


app = FastAPI(title="LogHub API")


@app.post("/logs", response_model=dict, summary="Ingestion d'un log")
async def create_log(log: LogEntry):
    
    # Nom de l'index selon la date du log (ou date du jour)
    dt = log.timestamp.date()
    index_name = f"logs-{dt.strftime('%Y.%m.%d')}"

    try:
        log_id = opensearch_client.index_log(index=index_name, document=log.dict())
        return {"id": log_id, **log.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexation failed: {e}")


@app.get(
    "/logs/search",
    response_model=List[dict],
    summary="Recherche full-text et filtres sur les logs"
)
async def search_logs(
    q: Optional[str] = Query(None, description="Recherche textuelle sur 'message'"),
    level: Optional[str] = Query(None, description="Filtrer par niveau"),
    service: Optional[str] = Query(None, description="Filtrer par service"),
    size: int = Query(10, ge=1, le=100, description="Nombre de résultats"),
    page: int = Query(1, ge=1, description="Numéro de page")
):
    
    # Préparation de la pagination
    from_ = (page - 1) * size

    # Construction des clauses de filtre
    must = []
    if q:
        must.append({"match": {"message": {"query": q}}})
    if level:
        must.append({"term": {"level.keyword": level}})
    if service:
        must.append({"term": {"service.keyword": service}})

    try:
        hits = opensearch_client.search_logs(
            index_pattern="logs-*",
            must_clauses=must,
            from_=from_,
            size=size
        )
        # Formatage de la réponse
        results = [
            {"id": h["_id"], **h["_source"]}
            for h in hits
        ]
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")
