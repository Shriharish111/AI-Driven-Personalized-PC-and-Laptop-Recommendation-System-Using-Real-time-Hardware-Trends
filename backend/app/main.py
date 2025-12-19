from fastapi import FastAPI

app = FastAPI(title="PC Recommendation System API")


@app.get("/health")
def health_check():
    return {"status": "Backend is running"}
