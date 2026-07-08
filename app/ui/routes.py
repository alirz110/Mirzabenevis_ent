
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

STATIC_DIR = Path(__file__).parent / "static"
INDEX_HTML_PATH = STATIC_DIR / "index.html"

@router.get("/", include_in_schema=False)
async def read_index():
    return FileResponse(INDEX_HTML_PATH)
