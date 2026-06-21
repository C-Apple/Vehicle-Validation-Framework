class Door:
    def __init__(self):
        self.door_locked_status = False

    def lock(self):
        self.door_locked_status = True
        return {"message": "Vehicle locked"}

    def unlock(self):
        self.door_locked_status = False
        return {"message": "Vehicle unlocked"}