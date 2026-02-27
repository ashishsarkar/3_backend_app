"""GET /api/locations/search — Elasticsearch-backed location autocomplete."""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.elasticsearch_client import search_locations

router = APIRouter()


@router.get("/search")
async def location_search(
    q: str = Query(..., min_length=1, description="Search query (city, airport code, state, country)"),
    type: Optional[str] = Query(None, description="Filter by type: city | state | country"),
    size: int = Query(8, ge=1, le=20),
):
    """
    Search locations using Elasticsearch.

    Returns cities, airports, Indian states, and countries matching the query.
    Supports fuzzy matching — typos are handled automatically.
    """
    if len(q.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query must not be empty")

    results = await search_locations(query=q.strip(), location_type=type, size=size)
    return {"query": q, "total": len(results), "results": results}
