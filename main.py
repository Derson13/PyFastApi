from fastapi import FastAPI
from app.api.endpoints import crop, supplier
from app.core.config import settings

app = FastAPI(title="Helios API")

# Include routers
app.include_router(crop.router, prefix=settings.API_V1_STR)
app.include_router(supplier.router, prefix=settings.API_V1_STR)
