from fastapi import FastAPI

app = FastAPI(
    title="RTC TEST SERVICE",
    version="0.1.0",
    description="""
Microservide TEST FastAPI

- Test de Health first heartbeat
"""
)


@app.get("/health")
async def health_check():
    """
    Basic heartbeat just to verify our service is alive
        """
    return {"status": "ok"}