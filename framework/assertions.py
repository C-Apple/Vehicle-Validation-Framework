from simulator.vehicle_state import Vehicle

#locks
def assert_doors_locked(vehicle: Vehicle):
    state = vehicle.get_state()

    assert state["locked"]

def assert_doors_unlocked(vehicle: Vehicle):
    state = vehicle.get_state()

    assert not state["locked"]

#awake status
def assert_vehicle_awake(vehicle: Vehicle):
    state = vehicle.get_state()

    assert state["awake"]

def assert_vehicle_asleep(vehicle: Vehicle):
    state = vehicle.get_state()

    assert not state["awake"]

# generic boolean status assertions (compare to expected)
def assert_awake_status(vehicle: Vehicle, expected: bool):
    state = vehicle.get_state()

    assert state["awake"] == expected

def assert_doors_locked_status(vehicle: Vehicle, expected: bool):
    state = vehicle.get_state()

    assert state["locked"] == expected

def assert_charging_status(vehicle: Vehicle, expected: bool):
    state = vehicle.get_state()

    assert state["charging"] == expected

def assert_climate_control_status(vehicle: Vehicle, expected: bool):
    state = vehicle.get_state()

    assert state["climate_control_on"] == expected

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

def assert_target_temp(vehicle: Vehicle, expected_temp: float | int):
    state = vehicle.get_state()

    assert state["target_temp"] == expected_temp

#transmission status
def assert_transmission_gear(vehicle: Vehicle, expected_gear):
    state = vehicle.get_state()

    assert state["transmission"] == expected_gear

#window status
def assert_window_percentage_open(vehicle: Vehicle, expected_percentage: float | int):
    state = vehicle.get_state()

    assert state["window"] == expected_percentage

def assert_window_closed(vehicle: Vehicle):
    state = vehicle.get_state()

    assert state["window"] == 0

def assert_window_open(vehicle: Vehicle):
    state = vehicle.get_state()

    assert state["window"] > 0

