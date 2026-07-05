from fastapi import FastAPI

app = FastAPI(
    title="TravelPlannerAgent API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {
        "message": "TravelPlannerAgent Backend Running"
    }