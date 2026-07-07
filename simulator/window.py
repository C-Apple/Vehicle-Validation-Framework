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

    @property
    def is_window_open(self):
        return self.window_open

    @property
    def window_open_percentage(self):
        return self.percentage_open