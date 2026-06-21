from fastapi import FastAPI
from .routes import router as vehicle_router
from simulator import Vehicle

app = FastAPI(title="Vehicle Automation Simulator")
vehicle_state = Vehicle()  # Create a global vehicle instance to maintain state across requests
app.include_router(vehicle_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Vehicle Automation Simulator API"}