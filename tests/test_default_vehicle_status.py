from simulator.vehicle_state import Vehicle
from simulator.transmission import Gear
import framework.exceptions as ex
from framework.config import (
    DEFAULT_AWAKE_STATUS,
    DEFAULT_DOOR_LOCKED_STATUS,
    DEFAULT_CHARGING_STATUS,
    DEFAULT_CLIMATE_CONTROL_ON,
    DEFAULT_TARGET_TEMP,
    DEFAULT_TRANSMISSION_GEAR,
    DEFAULT_WINDOW_PERCENTAGE_OPEN,
    DEFAULT_BATTERY_PERCENTAGE
)
def test_default_vehicle_state():
    vehicle = Vehicle()
    state = vehicle.get_state()

    assert state["battery_percentage"] == DEFAULT_BATTERY_PERCENTAGE
    assert state["awake"] == DEFAULT_AWAKE_STATUS
    assert state["locked"] == DEFAULT_DOOR_LOCKED_STATUS
    assert state["charging"] == DEFAULT_CHARGING_STATUS
    assert state["climate_control_on"] == DEFAULT_CLIMATE_CONTROL_ON
    assert state["target_temp"] == DEFAULT_TARGET_TEMP
    assert state["transmission"] == DEFAULT_TRANSMISSION_GEAR
    assert state["window"] == DEFAULT_WINDOW_PERCENTAGE_OPEN

def test_reset_vehicle_state():
    vehicle = Vehicle()
    vehicle.battery.set_battery_percentage(50)
    vehicle.sleep()
    vehicle.lock()
    vehicle.start_charging()
    vehicle.start_climate(70)
    vehicle.shift_gear(Gear.DRIVE)
    vehicle.window.percentage_open = 50

    vehicle.reset()

    state = vehicle.get_state()

    assert state["battery_percentage"] == DEFAULT_BATTERY_PERCENTAGE
    assert state["awake"] == DEFAULT_AWAKE_STATUS
    assert state["locked"] == DEFAULT_DOOR_LOCKED_STATUS
    assert state["charging"] == DEFAULT_CHARGING_STATUS
    assert state["climate_control_on"] == DEFAULT_CLIMATE_CONTROL_ON
    assert state["target_temp"] == DEFAULT_TARGET_TEMP
    assert state["transmission"] == DEFAULT_TRANSMISSION_GEAR
    assert state["window"] == DEFAULT_WINDOW_PERCENTAGE_OPEN