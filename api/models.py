from pydantic import BaseModel

class VehicleState(BaseModel):
    locked: bool = True
    awake: bool = False
    battery_percentage: int = 100
    charging: bool = False
    climate_control_on: bool = False

class CommandResponse(BaseModel):
    status: str
    reason: str | None = None