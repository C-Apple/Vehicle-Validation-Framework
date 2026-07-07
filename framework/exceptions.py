class VehicleException(Exception):
    """Base class for all vehicle exceptions."""
    pass

class BatteryDeadException(VehicleException):
    """Raised when an operation cannot be performed because the vehicle's battery is dead."""
    pass

class GearNotFoundException(VehicleException):
    """Raised when an operation cannot be performed because the gear is not found."""
    pass

class VehicleLockedException(VehicleException):
    """Raised when an operation cannot be performed because the vehicle is locked."""
    pass

class VehicleAsleepException(VehicleException):
    """Raised when an operation cannot be performed because the vehicle is asleep."""
    pass

class InvalidTemperatureException(VehicleException):
    """Raised when an operation cannot be performed because the temperature is invalid."""
    pass

class VehicleAwakeException(VehicleException):
    """Raised when an operation cannot be performed because the vehicle is awake."""
    pass

class BatteryLowException(VehicleException):
    """Raised when an operation cannot be performed because the vehicle's battery is low."""
    pass

class VehicleNotChargingException(VehicleException):
    """Raised when an operation cannot be performed because the vehicle is not charging."""
    pass