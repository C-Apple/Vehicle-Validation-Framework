from simulator import battery
from simulator.vehicle_state import Vehicle
import pytest
import framework.exceptions as ex

def test_door_locking_request_changes_vehicle_state():
    vehicle = Vehicle()
    
    vehicle.unlock()
    vehicle.lock()
    assert vehicle.doors_locked == True

def test_door_unlocking_request_changes_vehicle_state():
    vehicle = Vehicle()

    vehicle.lock()
    vehicle.unlock()
    assert vehicle.doors_locked == False

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

    assert vehicle.door.door_locked_status is True

def test_unlocking_wakes_vehicle():
    vehicle = Vehicle()
    vehicle.lock()
    vehicle.sleep()

    assert vehicle.awake == False

    vehicle.unlock()

    assert vehicle.awake == True