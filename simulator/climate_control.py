class ClimateControl:
    def __init__(self):
        self.climate_control_on = False
        self.target_temp = None
    
    def start_climate(self, target_temp: int = 72):
        self.climate_control_on = True
        self.target_temp = target_temp
        return {"message": "Climate control turned on"}
    
    def stop_climate(self):
        self.climate_control_on = False
        self.target_temp = None
        return {"message": "Climate control turned off"}