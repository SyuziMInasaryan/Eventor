import os
import uuid
import aiofiles
from fastapi import UploadFile, HTTPException

ALLOWED_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB

MEDIA_ROOT = "media"
EVENTS_DIR = "events"

async def save_event_image(image: UploadFile) -> str:
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported image type")

    ext = ALLOWED_TYPES[image.content_type]

    abs_dir = os.path.join(MEDIA_ROOT, EVENTS_DIR)
    os.makedirs(abs_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"

    rel_path = f"{EVENTS_DIR}/{filename}"  # это в БД
    abs_path = os.path.join(MEDIA_ROOT, rel_path)

    size = 0
    async with aiofiles.open(abs_path, "wb") as f:
        while True:
            chunk = await image.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_SIZE:
                try:
                    os.remove(abs_path)
                except FileNotFoundError:
                    pass
                raise HTTPException(status_code=400, detail="Image too large")
            await f.write(chunk)

    return rel_path
