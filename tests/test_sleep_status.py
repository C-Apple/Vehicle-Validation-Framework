from simulator.vehicle_state import Vehicle
import framework.assertions as a

def test_sleep_sets_vehicle_asleep():
    vehicle = Vehicle()

    vehicle.sleep()

    state = vehicle.get_state()
    a.assert_vehicle_asleep(vehicle)

def test_wake_sets_vehicle_awake():
    vehicle = Vehicle()

    vehicle.sleep()
    vehicle.wake()

    state = vehicle.get_state()
    a.assert_vehicle_awake(vehicle)