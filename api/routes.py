from fastapi import APIRouter
from app import vehicle_state

router = APIRouter(prefix="/vehicle", tags=["vehicle"])

@router.post("/vehicle/lock")
def lock_vehicle():
    vehicle_state["door_locked"] = True
    return {"message": "Vehicle locked"}

@router.post("/vehicle/unlock")
def unlock_vehicle():
    vehicle_state["door_locked"] = False
    return {"message": "Vehicle unlocked"}

@router.post("/vehicle/awake")
def wake_vehicle():
    vehicle_state["awake"] = True
    return {"message": "Vehicle is now awake"}

@router.post("/vehicle/sleep")
def sleep_vehicle():
    vehicle_state["awake"] = False
    return {"message": "Vehicle is now asleep"}

@router.post("/vehicle/charge")
def charge_vehicle():
    vehicle_state["charging"] = True
    return {"message": "Vehicle is now charging"}

@router.post("/vehicle/stop_charge")
def stop_charge_vehicle():
    vehicle_state["charging"] = False
    return {"message": "Vehicle has stopped charging"}