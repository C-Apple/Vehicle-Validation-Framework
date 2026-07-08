from simulator.vehicle_state import Vehicle
from simulator.transmission import Gear
import framework.assertions as a
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

    a.assert_battery_percentage(vehicle, DEFAULT_BATTERY_PERCENTAGE)
    a.assert_awake_status(vehicle, DEFAULT_AWAKE_STATUS)
    a.assert_doors_locked_status(vehicle, DEFAULT_DOOR_LOCKED_STATUS)
    a.assert_charging_status(vehicle, DEFAULT_CHARGING_STATUS)
    a.assert_climate_control_status(vehicle, DEFAULT_CLIMATE_CONTROL_ON)
    a.assert_target_temp(vehicle, DEFAULT_TARGET_TEMP)
    a.assert_transmission_gear(vehicle, DEFAULT_TRANSMISSION_GEAR)
    a.assert_window_percentage_open(vehicle, DEFAULT_WINDOW_PERCENTAGE_OPEN)

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

    a.assert_battery_percentage(vehicle, DEFAULT_BATTERY_PERCENTAGE)
    a.assert_awake_status(vehicle, DEFAULT_AWAKE_STATUS)
    a.assert_doors_locked_status(vehicle, DEFAULT_DOOR_LOCKED_STATUS)
    a.assert_charging_status(vehicle, DEFAULT_CHARGING_STATUS)
    a.assert_climate_control_status(vehicle, DEFAULT_CLIMATE_CONTROL_ON)
    a.assert_target_temp(vehicle, DEFAULT_TARGET_TEMP)
    a.assert_transmission_gear(vehicle, DEFAULT_TRANSMISSION_GEAR)
    a.assert_window_percentage_open(vehicle, DEFAULT_WINDOW_PERCENTAGE_OPEN)