from fastapi import APIRouter
from src.core.settings import Settings

router = APIRouter(tags=["Health"])

@router.get("/health", summary="Healthcheck")
async def healthcheck():
    settings = Settings()
    print(settings)
    return {"status": "ok"}

