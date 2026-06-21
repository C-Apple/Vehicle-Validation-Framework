from simulator.vehicle_state import Vehicle


def test_sleep_sets_vehicle_asleep():
    vehicle = Vehicle()

    vehicle.sleep()

    state = vehicle.get_state()
    assert state["awake"] is False

def test_wake_sets_vehicle_awake():
    vehicle = Vehicle()

    vehicle.sleep()
    vehicle.wake()

    state = vehicle.get_state()
    assert state["awake"] is True