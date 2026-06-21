from simulator import battery
from simulator.vehicle_state import Vehicle

def test_door_locking_request_changes_vehicle_state():
    vehicle = Vehicle()
    
    vehicle.unlock_door()
    vehicle.lock_door()
    assert vehicle.doors_locked == True

def test_door_unlocking_request_changes_vehicle_state():
    vehicle = Vehicle()

    vehicle.lock_door()
    vehicle.unlock_door()
    assert vehicle.doors_locked == False

def test_cannot_lock_when_battery_dead():
    vehicle = Vehicle()
    vehicle.unlock_door()

    vehicle.battery.set_battery_percentage(0)

    response = vehicle.lock()

    assert response.status_code == 400
    assert response.json()["detail"] == "Battery dead"

def test_cannot_unlock_when_battery_dead():
    vehicle = Vehicle()
    vehicle.lock_door()
    vehicle.battery.set_battery_percentage(0)

    response = vehicle.unlock()

    assert response.status_code == 400
    assert response.json()["detail"] == "Battery dead"