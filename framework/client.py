from simulator import battery, door, climate_control
import requests
from .logger import get_logger
from .config import BASE_URL

class VehicleClient:
        def __init__(self, base_url=BASE_URL):
            self.base_url = base_url
            self.logger = get_logger(__name__)

        def get_state(self):    
            response = requests.get(f"{self.base_url}/vehicle/state")
            self.logger.info("Get state called")
            return response.json()
        
        def lock(self):
            response = requests.post(f"{self.base_url}/vehicle/lock")
            self.logger.info("Lock called")
            return response.json()
        
        def unlock(self):
            response = requests.post(f"{self.base_url}/vehicle/unlock")
            self.logger.info("Unlock called")
            return response.json()
        
        def wake(self):
            response = requests.post(f"{self.base_url}/vehicle/awake")
            self.logger.info("Wake called")
            return response.json()
        
        def sleep(self):   
            response = requests.post(f"{self.base_url}/vehicle/sleep")
            self.logger.info("Sleep called")
            return response.json()