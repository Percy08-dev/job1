import os

class AbsPath:
    def __init__(self, path) -> None:
        base = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.normpath(os.path.join(base, path))

