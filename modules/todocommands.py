from enum import Enum, auto


class TodoCommand(Enum):
    """Todo Commands"""
    LIST = auto()
    NEW = auto()
    TOGGLE = auto()
    DELETE = auto()
    EXIT = auto()
    QUIT = EXIT