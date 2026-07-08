from simulator.vehicle_state import Vehicle
import pytest
import framework.exceptions as ex
import framework.assertions as a

def test_climate_turns_on():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(80)
    vehicle.start_climate(72)

    state = vehicle.get_state()
    a.assert_climate_control_on(vehicle)
    a.assert_target_temp(vehicle, 72)

def test_climate_rejects_invalid_temperature():
    vehicle = Vehicle()

    with pytest.raises(ex.InvalidTemperatureException):
        vehicle.start_climate(120)

def test_starting_climate_wakes_vehicle():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(80)
    vehicle.sleep()

    a.assert_vehicle_asleep(vehicle)

    vehicle.start_climate(72)

    a.assert_vehicle_awake(vehicle)

def test_climate_does_not_start_with_low_battery():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(3)

    with pytest.raises(ex.BatteryLowException):
        vehicle.start_climate(72)