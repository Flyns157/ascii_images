"""
This module provides utility functions and objects for the Image module.
"""


# =============================================== Imports ===============================================
from enum import Enum


# =============================================== Objects ===============================================
class AsciiGradient(Enum):
    """
    Enum class for the different gradients to use for the ASCII art.
    """
    LEVEL_10 = ' .:-=+*#@%'
    LEVEL_70 = ''' ."`^",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'''

    def __str__(self):
        return str(self.value)

    @classmethod
    def get_from_gscale(cls, gscale: int):
        """
        Get the AsciiGradient based on the grayscale level.

        Parameters:
            gscale (int): The grayscale level to use for the ASCII art. 0 for 10 levels of gray, 1 for ~70 levels of gray.

        Returns:
            AsciiGradient: The corresponding AsciiGradient object, or None if the gscale is invalid.
        """
        try:
            return cls(gscale)
        except ValueError as e:
            raise ValueError(f'Invalid gscale value: {gscale}. Expected 0 or 1.') from e


class GreyscaleMode(Enum):
    MIN = "min"
    LUMINANCE = "luminance"
    GREYSCALE = "greyscale"


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


class ColorLevel(int):
    """
    An integer type that is between 0 and 255.
    """
    def __new__(cls, value):
        if 0 <= value <= 255:
            raise ValueError(f'Expected an integer between 0 and 255, got {value}.')
        return int.__new__(cls, value)


class Color(tuple):
    def __new__(cls, r: ColorLevel, g: ColorLevel, b: ColorLevel):
        r = ColorLevel(r)
        g = ColorLevel(g)
        b = ColorLevel(b)
        return super().__new__(cls, (r, g, b))

    @property
    def r(self):
        return self[0]

    @property
    def g(self):
        return self[1]

    @property
    def b(self):
        return self[2]

    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b})"


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

    def __repr__(self):
        return f"Dimension(width={self.width}, height={self.height})"