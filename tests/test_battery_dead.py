from simulator.vehicle_state import Vehicle
import framework.assertions as a
from framework.config import CHARGE_STEP_INTERVAL

def test_battery_level_returns_correct_value():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(80)

    a.assert_battery_percentage(vehicle, 80)

def test_battery_level_can_be_updated():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(50)

    a.assert_battery_percentage(vehicle, 50)

def test_start_charging_sets_charging_state():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(50)

    vehicle.start_charging()

    a.assert_charging(vehicle)

def test_stop_charging_sets_charging_state_false():
    vehicle = Vehicle()

    vehicle.start_charging()

    vehicle.stop_charging()

    a.assert_not_charging(vehicle)

def test_charging_increases_battery():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(50)

    vehicle.start_charging()

    vehicle.simulate_charge_step()

    a.assert_battery_percentage(vehicle, 50 + CHARGE_STEP_INTERVAL)