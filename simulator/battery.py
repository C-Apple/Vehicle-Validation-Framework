from framework.config import LOW_BATTERY_THRESHOLD

class Battery:
    def __init__(self):
        self.percentage = 100
        self.charging = False

    def start_charging(self):
        self.charging = True

    def stop_charging(self):
        self.charging = False

    def simulate_charge_step(self):
        if self.charging:
            self.update_battery_percentage(1)  # Simulate a charge step of 1%

    def update_battery_percentage(self, amount):
        if self.charging:
            self.percentage = min(100, self.percentage + amount)

    #only use for tests
    def set_battery_percentage(self, percentage):
        if 0 <= percentage <= 100:
            self.percentage = percentage
        else:
            raise ValueError("Battery percentage must be between 0 and 100")

    @property
    def dead(self):
        return self.percentage <= 0
    
    @property
    def low(self):
        return self.percentage < LOW_BATTERY_THRESHOLD