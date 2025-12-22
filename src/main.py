from fastapi import FastAPI

from src.api.routers.category_routers import router as category_router
from src.api.routers.health import router as health_router
from src.api.routers.event_routers import router as event_router

app = FastAPI()

app.include_router(health_router)
app.include_router(category_router)
app.include_router(event_router)

