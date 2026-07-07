from simulator.vehicle_state import Vehicle
from simulator.battery import Battery
from simulator.climate_control import ClimateControl
import pytest
import framework.exceptions as ex

def test_climate_turns_on():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(80)
    vehicle.start_climate(72)

    state = vehicle.get_state()
    assert state["climate_control_on"] is True
    assert state["target_temp"] == 72

def test_climate_rejects_invalid_temperature():
    vehicle = Vehicle()

    with pytest.raises(ex.InvalidTemperatureException):
        vehicle.start_climate(120)

def test_starting_climate_wakes_vehicle():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(80)
    vehicle.sleep()

    assert vehicle.awake == False

    vehicle.start_climate(72)

    assert vehicle.awake == True


def test_climate_does_not_start_with_low_battery():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(3)

    with pytest.raises(ex.BatteryLowException):
        vehicle.start_climate(72)