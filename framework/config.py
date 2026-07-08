from simulator.transmission import Gear

BASE_URL = "http://127.0.0.1:8000/"
MIN_TEMP = 60
MAX_TEMP = 90
LOW_BATTERY_THRESHOLD = 10
VENT_PERCENTAGE = 15 #what percentage the window should be vented to when venting the window
CHARGE_STEP_INTERVAL = 5

#default status:
            #locked: False
            #awake: True
            #battery_percentage: 100
            #charging: False
            #climate_control_on: False
            #target_temp: None
            #transmission: PARK
            #window: 0% open

DEFAULT_DOOR_LOCKED_STATUS = False
DEFAULT_AWAKE_STATUS = True
DEFAULT_BATTERY_PERCENTAGE = 100
DEFAULT_CHARGING_STATUS = False
DEFAULT_CLIMATE_CONTROL_ON = False
DEFAULT_TARGET_TEMP = None
DEFAULT_TRANSMISSION_GEAR = Gear.PARK
DEFAULT_WINDOW_PERCENTAGE_OPEN = 0
