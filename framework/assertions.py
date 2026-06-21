

def assert_vehicle_state(vehicle):
    state = vehicle.get_state()
    assert state["locked"] == False, "Vehicle should be unlocked by default"
    assert state["awake"] == True, "Vehicle should be awake by default"
    assert state["battery_percentage"] == 100, "Battery percentage should be 100% by default"
    assert state["charging"] == False, "Vehicle should not be charging by default"
    assert state["climate_control_on"] == False, "Climate control should be off by default"