from enum import Enum
import numpy as np
from .color import ColorLevel, Color

class ProcessType(Enum):
    MIN = "min"
    MAX = "max"
    AVG = "avg"


class PositiveInt(int):
    """
    A positive integer type.
    """
    def __new__(cls, value):
        if value < 0:
            raise ValueError(f'Expected a positive integer, got {value}.')
        return int.__new__(cls, value)


class PositiveNotZeroInt(int):
    """
    A positive integer type that is not equal to 0.
    """
    def __new__(cls, value):
        if value <= 0:
            raise ValueError(f'Expected a positive integer, got {value}.')
        return int.__new__(cls, value)


class Percent(float):
    """
    A float type that is between 0 and 1.
    """
    def __new__(cls, value):
        if value < 0 or value > 1:
            raise ValueError(f'Expected a float between 0 and 1, got {value}.')
        return float.__new__(cls, value)


class Dimension(tuple):
    def __new__(cls, width: int, height: int):
        width = PositiveNotZeroInt(width)
        height = PositiveNotZeroInt(height)
        return super().__new__(cls, (width, height))

    @property
    def width(self):
        return self[0]

    @property
    def height(self):
        return self[1]
    
    def to_tuple(self):
        return (self.width, self.height)

    def __repr__(self):
        return f"Dimension(width={self.width}, height={self.height})"


type GrayScale = np.ndarray[np.dtype[ColorLevel]]