from fastapi import FastAPI
from sqlalchemy import create_engine
from src.database.models import Base
from src.core.settings import Settings

settings = Settings()
engine = create_engine(settings.db_url, echo=True)

app = FastAPI()

@app.get("/")
async def read_root():
    await some_long_io_task()
    return {"message": "Hello"}

Base.metadata.create_all(bind=engine)

print("✅ Таблицы успешно созданы.")