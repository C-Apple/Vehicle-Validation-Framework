class ClimateControl:
    def __init__(self):
        self.climate_control_on = False
    
    def turn_on(self):
        self.climate_control_on = True
        return {"message": "Climate control turned on"}
    
    def turn_off(self):
        self.climate_control_on = False
        return {"message": "Climate control turned off"}