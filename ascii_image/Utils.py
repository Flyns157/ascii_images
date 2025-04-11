"""
This module provides utility functions and objects for the Image module.
"""


# =============================================== Imports ===============================================
from enum import Enum
from PIL.ImageColor import getrgb


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


class Mode(Enum):
    MIN = "min"
    LUMINANCE = "luminance"
    GREYSCALE = "greyscale"
    TEXT_IMAGE = "text_image"


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
    def __new__(cls, *args):
        if len(args) == 1:
            if isinstance(args[0], str):
                # Cas : nom ou hexadécimal
                rgb = getrgb(args[0])  # lève une ValueError si invalide
            if isinstance(args[0], tuple):
                if len(args[0]) != 3:
                    raise ValueError("Color tuple must have 3 elements (r, g, b).")
                # Cas : tuple (r, g, b)
                rgb = tuple(map(ColorLevel,args[0]))
        elif len(args) == 3:
            # Cas : trois entiers RGB
            rgb = tuple(map(ColorLevel,args))
        else:
            raise ValueError("Color must be initialized with either 1 (str) or 3 (r, g, b) arguments.")
        
        return super().__new__(cls, rgb)

    @property
    def r(self): return self[0]
    @property
    def g(self): return self[1]
    @property
    def b(self): return self[2]

    def to_hex(self):
        return f"#{self[0]:02x}{self[1]:02x}{self[2]:02x}"

    def __repr__(self):
        return f"Color({self[0]}, {self[1]}, {self[2]})"


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


# ============================================== Functions ==============================================
...