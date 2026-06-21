from simulator.vehicle_state import Vehicle
from simulator.battery import Battery
from simulator.climate_control import ClimateControl

def test_climate_turns_on():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(80)
    vehicle.start_climate(72)

    state = vehicle.get_state()
    assert state["climate_control_on"] is True
    assert state["target_temp"] == 72

def test_climate_rejects_invalid_temperature():
    vehicle = Vehicle()

    response = vehicle.start_climate(120)

    assert response.status_code == 400

def test_climate_does_not_start_with_low_battery():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(3)

    response = vehicle.start_climate(72)

    assert response.status_code == 400