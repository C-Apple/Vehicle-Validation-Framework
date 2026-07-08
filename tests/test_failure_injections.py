import pytest

import framework.exceptions as ex
from framework.assertions import (
    assert_battery_not_dead,
    assert_battery_percentage,
    assert_detected_failure,
    assert_detected_failure_fields,
    assert_detected_failure_reason_contains,
    assert_doors_locked,
    assert_failure_injection_active,
    assert_no_detected_failures,
    assert_target_temp,
    assert_transmission_gear,
    assert_window_percentage_open,
)
from framework.config import DEFAULT_BATTERY_PERCENTAGE, MAX_TEMP, MIN_TEMP
from simulator.transmission import Gear
from simulator.vehicle_state import Vehicle


def test_invalid_battery_reading_falls_back_to_known_good_value():
    vehicle = Vehicle()
    vehicle.battery.set_battery_percentage(64)

    vehicle.inject_fault("battery_percentage", 145)

    assert_battery_percentage(vehicle, 64)
    assert_failure_injection_active(vehicle)
    assert_detected_failure_reason_contains(vehicle, "battery_percentage", "outside safe range 0-100")


def test_negative_battery_reading_does_not_create_false_dead_battery_status():
    vehicle = Vehicle()
    vehicle.battery.set_battery_percentage(50)
    vehicle.inject_fault("battery_percentage", -1)

    vehicle.lock()

    assert_doors_locked(vehicle)
    assert_battery_percentage(vehicle, 50)
    assert_battery_not_dead(vehicle)


def test_non_numeric_battery_reading_is_rejected():
    vehicle = Vehicle()
    vehicle.battery.set_battery_percentage(72)

    vehicle.inject_fault("battery_percentage", "full")

    assert_battery_percentage(vehicle, 72)
    assert_detected_failure(vehicle, "battery_percentage", "battery_percentage reading must be numeric")


def test_valid_battery_failure_injection_can_simulate_low_battery_reading():
    vehicle = Vehicle()
    vehicle.battery.set_battery_percentage(80)

    vehicle.inject_fault("battery_percentage", 8)

    assert_battery_percentage(vehicle, 8)
    assert_no_detected_failures(vehicle)


def test_out_of_range_window_reading_falls_back_to_actual_window_position():
    vehicle = Vehicle()
    vehicle.set_window_percentage(25)

    vehicle.inject_fault("window", 120)

    assert_window_percentage_open(vehicle, 25)
    assert_detected_failure(vehicle, "window")


def test_invalid_temperature_readings_fall_back_to_known_good_targets():
    vehicle = Vehicle()
    vehicle.start_climate(target_temp=72)

    vehicle.inject_fault("target_temp", MAX_TEMP + 20)
    assert_target_temp(vehicle, 72)
    assert_detected_failure(vehicle, "target_temp")

    vehicle.inject_fault("target_temp", MIN_TEMP - 20)
    assert_target_temp(vehicle, 72)
    assert_detected_failure(vehicle, "target_temp")


def test_invalid_boolean_reading_falls_back_to_actual_boolean_value():
    vehicle = Vehicle()
    vehicle.lock()

    vehicle.inject_fault("locked", "not really")

    assert_doors_locked(vehicle)
    assert_detected_failure(vehicle, "locked", "locked reading must be a boolean")


def test_invalid_transmission_reading_falls_back_to_actual_gear():
    vehicle = Vehicle()
    vehicle.shift_gear(Gear.DRIVE)

    vehicle.inject_fault("transmission", "P")

    assert_transmission_gear(vehicle, Gear.DRIVE)
    assert_detected_failure(vehicle, "transmission", "transmission reading must be a Gear value")


def test_multiple_failure_injections_report_each_detected_problem():
    vehicle = Vehicle()
    vehicle.battery.set_battery_percentage(88)
    vehicle.set_window_percentage(10)

    vehicle.inject_fault("battery_percentage", 101)
    vehicle.inject_fault("window", -5)

    assert_battery_percentage(vehicle, 88)
    assert_window_percentage_open(vehicle, 10)
    assert_detected_failure_fields(vehicle, {"battery_percentage", "window"})


def test_clear_fault_restores_normal_state_reporting():
    vehicle = Vehicle()
    vehicle.battery.set_battery_percentage(40)
    vehicle.inject_fault("battery_percentage", 200)

    vehicle.clear_fault("battery_percentage")

    assert_battery_percentage(vehicle, 40)
    assert_failure_injection_active(vehicle, expected=False)
    assert_no_detected_failures(vehicle)


def test_reset_clears_failure_injections():
    vehicle = Vehicle()
    vehicle.inject_fault("battery_percentage", 200)

    vehicle.reset()

    assert_failure_injection_active(vehicle, expected=False)
    assert_no_detected_failures(vehicle)
    assert_battery_percentage(vehicle, DEFAULT_BATTERY_PERCENTAGE)


def test_unknown_failure_injection_field_is_rejected():
    vehicle = Vehicle()

    with pytest.raises(ex.InvalidFailureInjectionException):
        vehicle.inject_fault("gps_altitude", 999999)
