from simulator import battery
from simulator.vehicle_state import Vehicle
import pytest
import framework.exceptions as ex
import framework.assertions as a

def test_door_locking_request_changes_vehicle_state():
    vehicle = Vehicle()
    
    vehicle.unlock()
    vehicle.lock()
    a.assert_doors_locked(vehicle)

def test_door_unlocking_request_changes_vehicle_state():
    vehicle = Vehicle()

    vehicle.lock()
    vehicle.unlock()
    a.assert_doors_unlocked(vehicle)

def test_cannot_lock_when_battery_dead():
    vehicle = Vehicle()
    vehicle.unlock()

    vehicle.battery.set_battery_percentage(0)

    with pytest.raises(ex.BatteryDeadException):
        vehicle.lock()

def test_cannot_unlock_when_battery_dead():
    vehicle = Vehicle()
    vehicle.lock()
    vehicle.battery.set_battery_percentage(0)

    with pytest.raises(ex.BatteryDeadException):
        vehicle.unlock()

    a.assert_doors_locked(vehicle)

def test_unlocking_wakes_vehicle():
    vehicle = Vehicle()
    vehicle.lock()
    vehicle.sleep()

    a.assert_vehicle_asleep(vehicle)

    vehicle.unlock()

    a.assert_vehicle_awake(vehicle)