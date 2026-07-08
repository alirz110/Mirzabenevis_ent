
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.routes import solver as api_solver_router
from app.ui import routes as ui_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG_MODE
)

app.include_router(api_solver_router.router, prefix="/api", tags=["Solver API"])

app.mount("/static", StaticFiles(directory="app/ui/static"), name="static")

app.include_router(ui_router.router, tags=["User Interface"])

@app.on_event("startup")
async def startup_event():
    logging.info(f"Application '{settings.APP_NAME}' startup complete.")
    logging.info(f"Debug mode is: {'ON' if settings.DEBUG_MODE else 'OFF'}")
