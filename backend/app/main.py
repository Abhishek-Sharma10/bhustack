from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import settings

app = FastAPI(
    title="BhuStack API",
    description=(
        "Parcel-centric land governance prototype. "
        "This prototype uses synthetic demonstration data and does not claim "
        "access to live government land records."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "name": "BhuStack",
        "message": "One Parcel. One Identity. Complete Land Intelligence.",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
