"""
This module provides a Color class that represents a color in RGB format.
"""

# =============================================== Imports ===============================================
from PIL.ImageColor import getrgb


# =============================================== Objects ===============================================
class ColorLevel(int):
    """
    An integer type that is between 0 and 255.
    """
    def __new__(cls, value):
        if 0 > value > 255:
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


# ============================================== Constants ==============================================
RED     = Color(255, 0, 0)
GREEN   = Color(0, 255, 0)
BLUE    = Color(0, 0, 255)
BLACK   = Color(0, 0, 0)
WHITE   = Color(255, 255, 255)