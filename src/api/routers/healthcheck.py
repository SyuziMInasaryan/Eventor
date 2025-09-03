from fastapi.responses import JSONResponse


@app.get("/health", summary="Healthcheck", tags=["Health"])
async def healthcheck():
    return JSONResponse(content={"status": "ok"})