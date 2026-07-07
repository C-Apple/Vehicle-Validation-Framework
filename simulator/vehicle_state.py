from simulator import battery, door, climate_control
from framework.config import MIN_TEMP, MAX_TEMP, LOW_BATTERY_THRESHOLD, CHARGE_STEP_INTERVAL, DEFAULT_BATTERY_PERCENTAGE, DEFAULT_AWAKE_STATUS, DEFAULT_DOOR_LOCKED_STATUS, DEFAULT_CHARGING_STATUS, DEFAULT_CLIMATE_CONTROL_ON, DEFAULT_TARGET_TEMP
import framework.exceptions as ex

class Vehicle:
    def __init__(self):
        #battery contains battery_percentage and charging status
        self.battery = battery.Battery()
        self.awake = True
        self.door = door.Door()
        self.climate_control = climate_control.ClimateControl()

    def get_state(self):
        return {
            "locked": self.door.door_locked_status,
            "awake": self.awake,
            "battery_percentage": self.battery.percentage,
            "charging": self.battery.charging,
            "climate_control_on": self.climate_control.climate_control_on,
            "target_temp": self.climate_control.target_temp

            #default status:
            #locked: False
            #awake: True
            #battery_percentage: 100
            #charging: False
            #climate_control_on: False
            #target_temp: None
        }
    
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
    
    def vehicle_reset(self):
        self.battery.set_battery_percentage(DEFAULT_BATTERY_PERCENTAGE)
        self.awake = DEFAULT_AWAKE_STATUS
        self.battery.charging = DEFAULT_CHARGING_STATUS
        self.door.door_locked_status = DEFAULT_DOOR_LOCKED_STATUS
        self.climate_control.target_temp = DEFAULT_TARGET_TEMP
        self.climate_control.climate_control_on = DEFAULT_CLIMATE_CONTROL_ON

        #default status:
            #locked: False
            #awake: True
            #battery_percentage: 100
            #charging: False
            #climate_control_on: False
            #target_temp: None

        return {"message": "Vehicle has been reset to default state"}
    
    
    #TODO: transmission integration: gear shift and current gear status

    #TODO: window integration & logic: venting logic, percentage open logic, etc.

    #fault injections
    def inject_fault(self, str):
    #TODO: Inject faults
        pass