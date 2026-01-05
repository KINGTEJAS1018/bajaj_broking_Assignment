# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import asyncio
import importlib
import sys, traceback
import logging
from app.services.limit_matcher import matcher_loop

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Lifespan Manager (Modern Replacement for on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the Limit Order Matcher in background
    logger.info("Starting Limit Matcher Background Task...")
    matcher_task = asyncio.create_task(matcher_loop())
    
    yield  # Application runs here
    
    # Shutdown: Clean up the background task
    logger.info("Shutting down Limit Matcher...")
    matcher_task.cancel()
    try:
        await matcher_task
    except asyncio.CancelledError:
        pass

# Initialize App with Lifespan
app = FastAPI(
    title="Bajaj Broking Trading API",
    version="1.0.0",
    description="Trading API Simulation using FastAPI (in-memory store)",
    lifespan=lifespan
)

def safe_include(module_path: str, router_name: str = "router", prefix: str = "/api/v1"):
    try:
        mod = importlib.import_module(module_path)
        router = getattr(mod, router_name)
        app.include_router(router, prefix=prefix)
        logger.info(f"[OK] Included router: {module_path}")
    except Exception as exc:
        logger.error(f"[ERROR] Failed to include router: {module_path}")
        traceback.print_exc(file=sys.stdout)

# Include Routers
safe_include("app.api.instruments")
safe_include("app.api.orders")
safe_include("app.api.trades")
safe_include("app.api.portfolio")
safe_include("app.api.ws")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "API is running"}