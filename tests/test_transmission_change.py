from simulator.vehicle_state import Vehicle
from simulator.transmission import Gear
import framework.exceptions as ex

def test_shift_gear():
    vehicle = Vehicle()

    vehicle.shift_gear(Gear.DRIVE)

    assert vehicle.current_gear == Gear.DRIVE

def test_shift_gear_with_dead_battery():
    vehicle = Vehicle()
    vehicle.battery.set_battery_percentage(0)
    
    try:
        vehicle.shift_gear(Gear.DRIVE)
        assert False, "Expected BatteryDeadException"
    except ex.BatteryDeadException:
        pass

def test_all_valid_gear_shifts():
    vehicle = Vehicle()

    for gear in Gear:
        vehicle.shift_gear(gear)
        assert vehicle.current_gear == gear

def test_shift_gear_with_invalid_gear():
    vehicle = Vehicle()

    try:
        vehicle.shift_gear("INVALID_GEAR")
        assert False, "Expected InvalidGearException"
    except ex.InvalidGearException:
        pass


#TODO: fix these tests and add more tests for transmission gear shifting and current gear status