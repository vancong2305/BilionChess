import os
class RootProgram:
    def __init__(self):
        # Get the absolute path to the current script file
        self.root_path = os.path.dirname(os.path.abspath(__file__))
    def get_root_path(self):
        return self.root_path