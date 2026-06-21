from simulator.vehicle_state import Vehicle

def test_battery_level_returns_correct_value():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(80)

    state = vehicle.get_state()

    assert state["battery_percentage"] == 80

def test_battery_level_can_be_updated():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(50)

    state = vehicle.get_state()

    assert state["battery_percentage"] == 50

def test_start_charging_sets_charging_state():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(50)

    vehicle.start_charging()

    state = vehicle.get_state()

    assert state["charging"] is True

def test_stop_charging_sets_charging_state_false():
    vehicle = Vehicle()

    vehicle.start_charging()

    vehicle.stop_charging()

    state = vehicle.get_state()

    assert state["charging"] is False

def test_charging_increases_battery():
    vehicle = Vehicle()

    vehicle.battery.set_battery_percentage(50)

    vehicle.start_charging()

    vehicle.simulate_charge_step()

    state = vehicle.get_state()

    assert state["battery_percentage"] > 50