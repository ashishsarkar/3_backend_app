from fastapi import APIRouter
from app.database import check_db_connection
from app.mongodb import ping_mongo

router = APIRouter()


@router.get("/live")
def live():
    return {"status": "ok"}


@router.get("/ready")
async def ready():
    pg_ok = check_db_connection()
    mongo_ok = await ping_mongo()
    overall = "ok" if (pg_ok and mongo_ok) else "degraded"
    return {
        "status": overall,
        "postgres": "ok" if pg_ok else "unreachable",
        "mongodb": "ok" if mongo_ok else "unreachable",
    }
