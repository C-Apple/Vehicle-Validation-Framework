import framework.exceptions as ex

class Window:
    def __init__(self):
        self.window_open = False
        self.percentage_open = 0  # Represents how much the window is open (0-100)

    def open_window(self):
        if self.window_open:
            return {"message": "Window is already open"}
        self.window_open = True
        self.percentage_open = 100
        return {"message": "Window opened"}

    def close_window(self):
        if not self.window_open:
            return {"message": "Window is already closed"}
        self.window_open = False
        self.percentage_open = 0
        return {"message": "Window closed"}
    
    def set_window_percentage(self, percentage):
        if not (0 <= percentage <= 100):
            raise ex.WindowPercentageException("Percentage must be between 0 and 100")
        self.percentage_open = percentage
        self.window_open = percentage > 0
        return {"message": f"Window set to {percentage}% open"}

    @property
    def is_window_open(self):
        return self.window_open