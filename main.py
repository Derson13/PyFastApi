from fastapi import FastAPI
from app.api.endpoints import *
from app.core.config import settings

app = FastAPI(title="Helios API")

# Include routers
app.include_router(crop, prefix=settings.API_V1_STR)
app.include_router(supplier, prefix=settings.API_V1_STR)
app.include_router(growing, prefix=settings.API_V1_STR)