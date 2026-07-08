from enum import Enum
import framework.exceptions as ex

class Gear(Enum):
    PARK = "P"
    REVERSE = "R"
    NEUTRAL = "N"
    DRIVE = "D"
    SPORT = "S"
    LOW = "L"

class Transmission:
    def __init__(self):
        self.current_gear = Gear.PARK

    def shift_gear(self, gear: Gear):
        if not isinstance(gear, Gear):
            raise ex.InvalidGearException("Invalid gear value")
        self.current_gear = gear
        return {"message": f"Shifted to {gear.value}"}
    
    @property
    def get_current_gear(self):
        return self.current_gear