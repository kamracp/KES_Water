from fastapi import FastAPI

app = FastAPI(
    title="Kamra Water OS",
    description="AI Powered Industrial Water, Wastewater and Utility Management Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "application": "Kamra Water OS",
        "status": "running",
        "version": "0.1.0",
        "product_model": "Engineering Operating System for Water Management",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Kamra Water OS backend",
    }
