"""FastAPI application for QA Generation from PDF"""
from fastapi import FastAPI
from app.api.routes import router
from app.core.config import MODEL_NAME, API_BASE

app = FastAPI(
    title="QA Generation API",
    version="1.0.0",
    description="Generate question-answer pairs from PDF documents"
)

app.include_router(router)

print(f"Initializing with:")
print(f"  Model: {MODEL_NAME}")
print(f"  API Base: {API_BASE}")
print("Pipeline ready!\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
