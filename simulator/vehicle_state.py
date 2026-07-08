from simulator import battery, door, climate_control, transmission, window
import framework.exceptions as ex
from framework.config import (
    CHARGE_STEP_INTERVAL,
    DEFAULT_BATTERY_PERCENTAGE,
    MIN_TEMP,
    MAX_TEMP,
    LOW_BATTERY_THRESHOLD,
    DEFAULT_AWAKE_STATUS,
    DEFAULT_DOOR_LOCKED_STATUS,
    DEFAULT_CHARGING_STATUS,
    DEFAULT_CLIMATE_CONTROL_ON,
    DEFAULT_TARGET_TEMP,
    DEFAULT_TRANSMISSION_GEAR,
    DEFAULT_WINDOW_PERCENTAGE_OPEN,
    VENT_PERCENTAGE
)

class Vehicle:
    _READING_LIMITS = {
        "battery_percentage": (0, 100),
        "window": (0, 100),
        "target_temp": (MIN_TEMP, MAX_TEMP),
    }
    _BOOLEAN_READINGS = {"locked", "awake", "charging", "climate_control_on"}

    def __init__(self):
        #battery contains battery_percentage and charging status
        self.battery = battery.Battery()
        self.awake = True
        self.door = door.Door()
        self.climate_control = climate_control.ClimateControl()
        self.transmission = transmission.Transmission()
        self.window = window.Window()
        self._failure_injections = {}
        self._last_detected_failures = []

    def _raw_state(self):
        return {
            "locked": self.door.door_locked_status,
            "awake": self.awake,
            "battery_percentage": self.battery.percentage,
            "charging": self.battery.charging,
            "climate_control_on": self.climate_control.climate_control_on,
            "target_temp": self.climate_control.target_temp,
            "transmission": self.transmission.get_current_gear,
            "window": self.window.percentage_open
        }

    def _safe_reading(self, field, value, known_good):
        if field in self._BOOLEAN_READINGS and not isinstance(value, bool):
            return known_good, f"{field} reading must be a boolean"

        if field in self._READING_LIMITS:
            if value is None and field == "target_temp":
                return value, None
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                return known_good, f"{field} reading must be numeric"
            minimum, maximum = self._READING_LIMITS[field]
            if value < minimum or value > maximum:
                return known_good, f"{field} reading {value} is outside safe range {minimum}-{maximum}"

        if field == "transmission" and not isinstance(value, transmission.Gear):
            return known_good, "transmission reading must be a Gear value"

        return value, None

    def get_state(self):
        raw_state = self._raw_state()
        reported_state = raw_state.copy()
        detected_failures = []

        for field, injected_value in self._failure_injections.items():
            safe_value, failure = self._safe_reading(field, injected_value, raw_state[field])
            reported_state[field] = safe_value
            if failure:
                detected_failures.append({
                    "field": field,
                    "injected_value": injected_value,
                    "safe_value": safe_value,
                    "reason": failure,
                })

        self._last_detected_failures = detected_failures
        reported_state["failure_injection_active"] = bool(self._failure_injections)
        reported_state["detected_failures"] = detected_failures
        return reported_state
    
    def lock(self):
        # check if battery dead before locking
        if self.battery.dead:
            raise ex.BatteryDeadException("Cannot lock vehicle: Battery is dead")

        return self.door.lock()
    
    @property
    def doors_locked(self):
        return self.door.door_locked_status
    
    def unlock(self):
        # check if battery dead before unlocking
        if self.battery.dead:
            raise ex.BatteryDeadException("Cannot unlock vehicle: Battery is dead")
        
        self.awake = True  # Unlocking the door wakes the vehicle

        return self.door.unlock()
    
    @property
    def doors_unlocked(self):
        return not self.door.door_locked_status

    def wake(self):
        # check if battery dead before waking
        if self.battery.dead:
            raise ex.BatteryDeadException("Cannot wake vehicle: Battery is dead")

        self.awake = True
        return {"message": "Vehicle is now awake"}
    
    def sleep(self):
        self.awake = False
        return {"message": "Vehicle is now asleep"}
    
    def start_charging(self):
        self.battery.start_charging()
        return {"message": "Vehicle is now charging"}
    
    def stop_charging(self):
        self.battery.stop_charging()
        return {"message": "Vehicle has stopped charging"}
    
    def simulate_charge_step(self):
        if not self.battery.charging:
            raise ex.VehicleNotChargingException("Cannot simulate charge step: Vehicle is not charging")
        self.battery.update_battery_percentage(CHARGE_STEP_INTERVAL)
        return {"message": "Battery percentage updated by {}%".format(CHARGE_STEP_INTERVAL)}
    
    def start_climate(self, target_temp = 72):
        # check if battery dead before turning on climate control
        if self.battery.dead:
            raise ex.BatteryDeadException("Cannot turn on climate control: Battery is dead")
        
        if self.battery.percentage < LOW_BATTERY_THRESHOLD:
            raise ex.BatteryLowException("Cannot turn on climate control: Battery percentage is too low")
        
        if target_temp < MIN_TEMP or target_temp > MAX_TEMP:
            raise ex.InvalidTemperatureException("Target temperature must be between {} and {} degrees Fahrenheit".format(MIN_TEMP, MAX_TEMP))
        self.awake = True  # Starting climate control wakes the vehicle
        self.climate_control.start_climate(target_temp)
        return {"message": "Climate control is now on; target temperature set to {}".format(target_temp)}
    
    def stop_climate(self):
        self.climate_control.stop_climate()
        return {"message": "Climate control is now off"}

    def shift_gear(self, gear):
        # check if battery dead before shifting gear
        if self.battery.dead:
            raise ex.BatteryDeadException("Cannot shift gear: Battery is dead")
        
        self.transmission.shift_gear(gear)
        return {"message": "Transmission gear shifted to {}".format(gear)}
    
    @property
    def current_gear(self):
        return self.transmission.get_current_gear

    def set_window_percentage(self, percentage):
        # check if battery dead before setting window percentage
        if self.battery.dead:
            raise ex.BatteryDeadException("Cannot set window percentage: Battery is dead")
        
        self.window.set_window_percentage(percentage)
        return {"message": "Window open percentage set to {}".format(percentage)}
    
    def close_window(self):
        # check if battery dead before closing window
        if self.battery.dead:
            raise ex.BatteryDeadException("Cannot close window: Battery is dead")
        
        self.window.close_window()
        return {"message": "Window is now closed"}

    def open_window(self):
        # check if battery dead before opening window
        if self.battery.dead:
            raise ex.BatteryDeadException("Cannot open window: Battery is dead")
        
        self.window.open_window()
        return {"message": "Window is now open"}
    
    def vent_window(self):
        # check if battery dead before venting window
        if self.battery.dead:
            raise ex.BatteryDeadException("Cannot vent window: Battery is dead")
        
        self.window.set_window_percentage(VENT_PERCENTAGE)
        return {"message": "Window is now vented"}
    
    @property
    def window_percentage_open(self):
        return self.window.percentage_open

    #fault injections
    def inject_fault(self, field, value=None):
        raw_state = self._raw_state()
        if field not in raw_state:
            raise ex.InvalidFailureInjectionException("Unknown failure injection field: {}".format(field))
        self._failure_injections[field] = value
        return {"message": "Failure injection set for {}".format(field)}

    def clear_fault(self, field=None):
        if field is None:
            self._failure_injections.clear()
            self._last_detected_failures = []
            return {"message": "All failure injections cleared"}

        if field not in self._failure_injections:
            raise ex.InvalidFailureInjectionException("No failure injection is set for {}".format(field))

        del self._failure_injections[field]
        self._last_detected_failures = []
        return {"message": "Failure injection cleared for {}".format(field)}

    @property
    def detected_failures(self):
        return self._last_detected_failures

    def reset(self):
        self.battery.set_battery_percentage(DEFAULT_BATTERY_PERCENTAGE)
        self.awake = DEFAULT_AWAKE_STATUS
        self.battery.charging = DEFAULT_CHARGING_STATUS
        self.door.door_locked_status = DEFAULT_DOOR_LOCKED_STATUS
        self.climate_control.target_temp = DEFAULT_TARGET_TEMP
        self.climate_control.climate_control_on = DEFAULT_CLIMATE_CONTROL_ON
        self.transmission.current_gear = DEFAULT_TRANSMISSION_GEAR
        self.window.percentage_open = DEFAULT_WINDOW_PERCENTAGE_OPEN
        self._failure_injections.clear()
        self._last_detected_failures = []

        #default status:
            #locked: False
            #awake: True
            #battery_percentage: 100
            #charging: False
            #climate_control_on: False
            #target_temp: None
            #transmission: PARK
            #window: 0% open

        return {"message": "Vehicle has been reset to default state"}