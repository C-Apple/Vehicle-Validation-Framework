from simulator import battery, door, climate_control

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
            "awake": self.climate_control.climate_control_on,
            "battery_percentage": self.battery.percentage,
            "charging": self.battery.charging,
            "climate_control_on": self.climate_control.climate_control_on

            #default status:
            #locked: False
            #awake: True
            #battery_percentage: 100
            #charging: False
            #climate_control_on: False
        }
    
    def lock(self):
        # check if battery dead before locking
        if self.battery.dead:
            raise Exception("Cannot lock vehicle: Battery is dead")

        return self.door.lock()
    
    def unlock(self):
        # check if battery dead before unlocking
        if self.battery.dead:
            raise Exception("Cannot unlock vehicle: Battery is dead")

        return self.door.unlock()
    
    def wake(self):
        # check if battery dead before waking
        if self.battery.dead:
            raise Exception("Cannot wake vehicle: Battery is dead")

        self.awake = True
        return {"message": "Vehicle is now awake"}
    
    def sleep(self):
        self.awake = False
        return {"message": "Vehicle is now asleep"}
    
    def charge(self):
        self.battery.start_charging()
        return {"message": "Vehicle is now charging"}
    
    def stop_charge(self):
        self.battery.stop_charging()
        return {"message": "Vehicle has stopped charging"}
    
    def turn_on_climate_control(self):
        # check if battery dead before turning on climate control
        if self.battery.dead:
            raise Exception("Cannot turn on climate control: Battery is dead")

        self.climate_control.turn_on()
        return {"message": "Climate control is now on"}
    
    def turn_off_climate_control(self):
        self.climate_control.turn_off()
        return {"message": "Climate control is now off"}