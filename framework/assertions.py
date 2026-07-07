from simulator import Vehicle

#locks
def assert_doors_locked(vehicle: Vehicle):
    state = vehicle.get_state()

    assert state["doors_locked"]

def assert_doors_unlocked(vehicle: Vehicle):
    state = vehicle.get_state()

    assert not state["doors_locked"]

#awake status
def assert_vehicle_awake(vehicle: Vehicle):
    state = vehicle.get_state()

    assert state["awake"]

def assert_vehicle_asleep(vehicle: Vehicle):
    state = vehicle.get_state()

    assert not state["awake"]

#battery status
def assert_battery_percentage(vehicle: Vehicle, expected_percentage: float | int):
    state = vehicle.get_state()

    assert state["battery_percentage"] == expected_percentage

def assert_charging(vehicle: Vehicle):
    state = vehicle.get_state()

    assert state["charging"]

def assert_not_charging(vehicle: Vehicle):
    state = vehicle.get_state()

    assert not state["charging"]

def assert_battery_above_threshold(vehicle: Vehicle, threshold: float | int):
    state = vehicle.get_state()

    assert state["battery_percentage"] > threshold

#climate control status
def assert_climate_control_on(vehicle: Vehicle):
    state = vehicle.get_state()

    assert state["climate_control_on"]

def assert_climate_control_off(vehicle: Vehicle):
    state = vehicle.get_state()

    assert not state["climate_control_on"]