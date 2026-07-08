from simulator.vehicle_state import Vehicle
import framework.exceptions as ex

def test_open_window_changes_vehicle_state():
    vehicle = Vehicle()
    
    vehicle.set_window_percentage(50)
    assert vehicle.window.percentage_open == 50

def test_close_window_changes_vehicle_state():
    vehicle = Vehicle()
    
    vehicle.set_window_percentage(50)
    vehicle.set_window_percentage(0)
    assert vehicle.window.percentage_open == 0