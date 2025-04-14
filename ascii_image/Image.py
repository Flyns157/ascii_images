"""
This module provides functions to represent an image as ASCII art or reverse.
"""

# =============================================== Imports ===============================================
from PIL.Image import Image, fromarray
import numpy as np

from .types import (
    ProcessType,
    GrayScale
)


# ============================================== Functions ==============================================
def grayscale_to_image(
        grayscale : GrayScale
    )-> Image :
    """
    Converts a greyscale numpy array into an image.

    Parameters:
        grayscale (GreyScale): The greyscale numpy array to convert.

    Returns:
        Image: The image object.
    """
    return fromarray(grayscale.astype(np.uint8), mode='L')


def image_to_grayscale(
        img : Image,
        grayscale_mode : ProcessType = ProcessType.AVG
    )-> GrayScale :
    """
    Converts an image into a greyscale numpy array.

    Parameters:
        img (Image):                            The image object to convert.
        grayscale_mode (ProcessType, optional): The mode to use for computing the grayscale value of each pixel. Defaults to ProcessType.AVG.

    Returns:
        GreyScale: The greyscale numpy array.
    """
    # Compute grayscale
    arr = np.array(img.convert("RGB"))
    match grayscale_mode:
        case ProcessType.AVG: return arr.mean(axis=2)
        case ProcessType.MAX: return arr.max(axis=2)
        case ProcessType.MIN: return arr.min(axis=2)
        case _: raise ValueError(f'Invalid greyscale mode: {grayscale_mode}.')
