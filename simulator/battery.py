class Battery:
    def __init__(self):
        self.percentage = 100
        self.charging = False

    def start_charging(self):
        self.charging = True

    def stop_charging(self):
        self.charging = False

    def update_battery_percentage(self, amount):
        if self.charging:
            self.percentage = min(100, self.percentage + amount)
        else:
            self.percentage = max(0, self.percentage - amount)

    @property
    def dead(self):
        return self.percentage <= 0