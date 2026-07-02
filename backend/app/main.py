from fastapi import FastAPI

from app.api.routes.water_balance import router as water_balance_router
from app.api.routes.pump_selection import router as pump_selection_router

app = FastAPI(
    title="Kamra Water OS",
    description="AI Powered Industrial Water, Wastewater & Utility Management Platform",
    version="0.1.0",
)

app.include_router(water_balance_router)
app.include_router(pump_selection_router)


@app.get("/")
def root():
    return {
        "application": "Kamra Water OS",
        "status": "running",
        "version": "0.1.0",
        "product_model": "Engineering Operating System for Water Management",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Kamra Water OS Backend",
    }