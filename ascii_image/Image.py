"""
This module provides functions to represent an image as ASCII art or reverse.
"""


# =============================================== Imports ===============================================
import os
from PIL import ImageDraw, ImageFont
from PIL.Image import Image, open as open_image, new as new_image, fromarray
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np

from .Utils import (
    AsciiGradient,
    ProcessType,
    PositiveInt,
    PositiveNotZeroInt,
    Percent,
    ColorLevel,
    Color,
    Dimension,
    GrayScale
)

from warnings import deprecated


# ============================================== Functions ==============================================

def ascii_to_grayscale(
        ascii_art : str,
        ascii_gradient : AsciiGradient = AsciiGradient.LEVEL_10
    )-> GrayScale :
    """
    Converts an ASCII Art string into a greyscale numpy array.

    Parameters:
        ascii_art (str):                            The ASCII art string to convert.
        ascii_gradient (AsciiGradient, optional):   The ASCII gradient to use. Defaults to AsciiGradient.LEVEL_10.

    Returns:
        GreyScale: The greyscale numpy array.
    """
    n = 255 / (len(ascii_gradient.value) - 1)
    indexed_gradient = {c:i for i,c in enumerate(ascii_gradient.value)}

    lines = ascii_art.split('\n')
    arr = np.zeros((len(lines), max(len(line) for line in lines)), dtype=ColorLevel)

    for y, line in enumerate(lines) :
        for x, char in enumerate(line) :
            arr[y,x] = indexed_gradient[char]*n
    return arr

def grayscale_to_ascii(
        grayscale : GrayScale,
        ascii_gradient : AsciiGradient = AsciiGradient.LEVEL_10,
        space : PositiveInt = 0
    )-> str :
    """
    Converts a greyscale numpy array into an ASCII Art string.

    Parameters:
        greyscale (GreyScale):                      The greyscale numpy array to convert.
        ascii_gradient (AsciiGradient, optional):   The ASCII gradient to use. Defaults to AsciiGradient.LEVEL_10.
        space (PositiveInt, optional):              The number of spaces to add between ASCII characters. Defaults to 0.

    Returns:
        str: The ASCII art string.
    """
    # Normalize to ASCII gradient indices
    n = (len(ascii_gradient.value) - 1) / 255
    scaled = (grayscale * n).astype(int)

    # Map values to ASCII characters
    chars = np.array(list(ascii_gradient.value))[scaled]

    if space > 0: chars = np.char.add(chars, ' ' * space)

    # Join rows
    return '\n'.join(''.join(row) for row in chars)


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
        img (Image): The image object to convert.
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


def image_to_ascii(
        img: Path | Image,
        ascii_gradient: AsciiGradient = AsciiGradient.LEVEL_10,
        output_dimensions: Dimension | Percent = Dimension(50, 50),
        output_file: Path = None,
        grayscale_mode: ProcessType = ProcessType.AVG, 
        space: PositiveInt = 0
    ) -> str:
    """
    Converts an image to ASCII art and optionally writes it to a file and returns it as a string.

    Parameters:
        img (Path | Image):                                 The path to the input image file or the image object itself.
        ascii_gradient (AsciiGradient, optional):           The ASCII gradient to use. Defaults to AsciiGradient.LEVEL_10.
        output_dimensions (Dimension | Percent, optional):  The dimensions of the output image. If a float, it is interpreted as a percentage of the input image dimensions. Defaults to Dimension(50, 50).
        output_file (Path, optional):                       The path to the output text file if outpout_in_file is True. Defaults to None.
        grayscale_mode (GreyscaleProcessType, optional):           The mode to use for computing the grayscale value of each pixel. Defaults to GreyscaleProcessType.AVG.
        space (PositiveInt, optional):                      The number of spaces to add between ASCII characters. Defaults to 0.

    Returns:
        str: The ASCII art as a string.
    """
    # Check input types and values
    img_must_be_closed = False
    if isinstance(img, (str, Path)): img, img_must_be_closed = open_image(Path(img)), True
    if not isinstance(ascii_gradient, AsciiGradient): raise TypeError(f'Expected an AsciiGradient, got {type(ascii_gradient)}.')
    output_dimensions = (int(img.width * output_dimensions), int(img.height * output_dimensions)) if isinstance(output_dimensions, float) else Dimension(*output_dimensions)
    space = PositiveInt(space)

    # Convert to ASCII art
    ascii_art = grayscale_to_ascii(
        # Compute grayscale
        grayscale=image_to_grayscale(
            img.resize(output_dimensions),
            grayscale_mode
        ),
        ascii_gradient=ascii_gradient,
        space=space
    )

    # Save to file
    if output_file is not None:
        with open(output_file, 'w') as f: f.write(ascii_art)
    
    if img_must_be_closed: img.close()
    return ascii_art


def process_images(images_files):
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(image_to_ascii, image_file) for image_file in images_files]
        return [future.result()for future in futures]


def ascii_to_image(
        ascii_art : str,
        output_mode: str = "text_image",
        ascii_gradient: AsciiGradient = AsciiGradient.LEVEL_10,
        font_file : str = None,
        font_size : float = 1.0,
        text_color : Color = Color(100, 255, 100),
        bg_color : Color = Color(0, 0, 0),
        compression : int = 5,
        output_file : str | Path = None,
)-> Image :
    """
    Converts an ASCII Art string into an image and saves it to a file.

    Parameters:
        ascii_art (str):                            The ASCII art string to convert.
        output_mode (ProcessType, optional):               The mode to use for the output image. Defaults to ProcessType.TEXT_IMAGE.
        ascii_gradient (AsciiGradient, optional):   The ASCII gradient to use. Defaults to AsciiGradient.LEVEL_10.
        font_file (str, optional):                  The path to the font file to use. Defaults to 'font/MonospaceTypewriter.ttf'.
        font_size (float, optional):                The font size to use. Defaults to 1.0.
        text_color (Color, optional):               The color of the text. Defaults to Color(100, 255, 100).
        bg_color (Color, optional):                 The color of the background. Defaults to Color(0, 0, 0).
        compression (int, optional):                The compression factor to use. Defaults to 5.
        output_file (str | Path, optional):         The path to the output file. Defaults to 'ascii_art.png'.

    Returns:
        Image: The output image object.
    """
    match output_mode:
        case "text_image":
            lines = ascii_art.split('\n')
            img = new_image('RGB', (max([len(line) for line in lines])*compression,len(lines)*compression), color = bg_color)
            drawer = ImageDraw.Draw(img)
            for y, line in enumerate(lines) :
                for x, char in enumerate(line) :
                    drawer.text((x*compression, y*compression), char, font=ImageFont.truetype(font_file, int(font_size*compression)), fill=text_color)
            if output_file is not None: img.save(output_file)
            return img
        case "grayscale_image":
            img = grayscale_to_image(
                ascii_to_grayscale(
                    ascii_art,
                    ascii_gradient if ascii_gradient is not None else ...
                )
            )
        case _: raise ValueError(f'Invalid output mode: {output_mode}.')
    if output_file is not None: img.save(output_file)
    return img


def process_ascii_art(ascii_arts, outputs_files):
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(ascii_to_image, ascii_art, output_file) for ascii_art, output_file in zip(ascii_arts, outputs_files)]
        return [future.result()for future in futures]

def ascii_to_greyimg(ascii_art : str, outpout_file : str = 'ascii_art.png', text_color : tuple[int,int,int] | str = (100, 255, 100), bg_color : tuple[int,int,int] | str = (0, 0, 0), compression : int = 5, font_file : str = 'font/MonospaceTypewriter.ttf', font_size : float = 1.0)-> Image | None :
    raise NotImplementedError("This function is not yet implemented.")