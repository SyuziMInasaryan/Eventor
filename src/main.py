import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.category_routers import router as category_router
from src.api.routers.health import router as health_router
from src.api.routers.event_routers import router as event_router
from src.api.routers.user_routers import router as user_router
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на dev ок
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(category_router)
app.include_router(event_router)

app.include_router(user_router)

os.makedirs("media/events", exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")

