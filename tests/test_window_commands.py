from simulator.vehicle_state import Vehicle
import framework.exceptions as ex
import framework.assertions as a

def test_open_window_changes_vehicle_state():
    vehicle = Vehicle()
    
    vehicle.set_window_percentage(50)
    a.assert_window_percentage_open(vehicle, 50)

def test_close_window_changes_vehicle_state():
    vehicle = Vehicle()
    
    vehicle.set_window_percentage(50)
    vehicle.set_window_percentage(0)
    a.assert_window_closed(vehicle)