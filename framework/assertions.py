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


#failure injection status
def assert_failure_injection_active(vehicle: Vehicle, expected: bool = True):
    state = vehicle.get_state()

    assert state["failure_injection_active"] is expected


def assert_no_detected_failures(vehicle: Vehicle):
    state = vehicle.get_state()

    assert state["detected_failures"] == []


def assert_detected_failure(vehicle: Vehicle, expected_field: str, expected_reason: str | None = None):
    state = vehicle.get_state()
    matching_failures = [
        failure for failure in state["detected_failures"]
        if failure["field"] == expected_field
    ]

    assert matching_failures, f"Expected detected failure for {expected_field}"
    if expected_reason is not None:
        assert matching_failures[0]["reason"] == expected_reason


def assert_detected_failure_reason_contains(vehicle: Vehicle, expected_field: str, expected_reason_text: str):
    state = vehicle.get_state()
    matching_failures = [
        failure for failure in state["detected_failures"]
        if failure["field"] == expected_field
    ]

    assert matching_failures, f"Expected detected failure for {expected_field}"
    assert expected_reason_text in matching_failures[0]["reason"]


def assert_detected_failure_fields(vehicle: Vehicle, expected_fields: set[str]):
    state = vehicle.get_state()

    assert {failure["field"] for failure in state["detected_failures"]} == expected_fields


def assert_battery_not_dead(vehicle: Vehicle):
    assert vehicle.battery.dead is False
