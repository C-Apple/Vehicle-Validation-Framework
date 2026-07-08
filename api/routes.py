from enum import Enum
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import framework.exceptions as vehicle_exceptions
from simulator.transmission import Gear
from simulator.vehicle_state import Vehicle


router = APIRouter(prefix="/vehicle", tags=["vehicle"])
vehicle_state = Vehicle()


class ClimateRequest(BaseModel):
    target_temp: int = 72


class WindowRequest(BaseModel):
    percentage: int


class GearRequest(BaseModel):
    gear: str


class FaultRequest(BaseModel):
    field: str
    value: Any = None


def _serialize_value(value):
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, list):
        return [_serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize_value(item) for key, item in value.items()}
    return value


def _state_payload(message=None):
    payload = {
        "message": message,
        "state": _serialize_value(vehicle_state.get_state()),
    }
    return payload


def _run_command(command, *args, **kwargs):
    try:
        result = command(*args, **kwargs)
    except vehicle_exceptions.VehicleException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return _state_payload(result.get("message") if isinstance(result, dict) else None)


@router.get("/state")
def get_vehicle_state():
    return _state_payload()


@router.post("/lock")
def lock_vehicle():
    return _run_command(vehicle_state.lock)


@router.post("/unlock")
def unlock_vehicle():
    return _run_command(vehicle_state.unlock)


@router.post("/wake")
def wake_vehicle():
    return _run_command(vehicle_state.wake)


@router.post("/awake")
def awake_vehicle():
    return wake_vehicle()


@router.post("/sleep")
def sleep_vehicle():
    return _run_command(vehicle_state.sleep)


@router.post("/charge/start")
def start_charging():
    return _run_command(vehicle_state.start_charging)


@router.post("/charge")
def charge_vehicle():
    return start_charging()


@router.post("/charge/stop")
def stop_charging():
    return _run_command(vehicle_state.stop_charging)


@router.post("/stop_charge")
def stop_charge_vehicle():
    return stop_charging()


@router.post("/charge/step")
def simulate_charge_step():
    return _run_command(vehicle_state.simulate_charge_step)


@router.post("/climate/start")
def start_climate(request: ClimateRequest):
    return _run_command(vehicle_state.start_climate, request.target_temp)


@router.post("/climate/stop")
def stop_climate():
    return _run_command(vehicle_state.stop_climate)


@router.post("/window/open")
def open_window():
    return _run_command(vehicle_state.open_window)


@router.post("/window/close")
def close_window():
    return _run_command(vehicle_state.close_window)


@router.post("/window/vent")
def vent_window():
    return _run_command(vehicle_state.vent_window)


@router.post("/window/set")
def set_window_percentage(request: WindowRequest):
    return _run_command(vehicle_state.set_window_percentage, request.percentage)


@router.post("/transmission/shift")
def shift_transmission(request: GearRequest):
    try:
        gear = Gear[request.gear.upper()]
    except KeyError:
        try:
            gear = Gear(request.gear.upper())
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid gear value") from exc

    return _run_command(vehicle_state.shift_gear, gear)


@router.post("/faults")
def inject_fault(request: FaultRequest):
    return _run_command(vehicle_state.inject_fault, request.field, request.value)


@router.delete("/faults")
def clear_all_faults():
    return _run_command(vehicle_state.clear_fault)


@router.delete("/faults/{field}")
def clear_fault(field: str):
    return _run_command(vehicle_state.clear_fault, field)


@router.post("/reset")
def reset_vehicle():
    return _run_command(vehicle_state.reset)
