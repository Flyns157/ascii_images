"""
This module provides functions to represent an image as ASCII art or reverse.
"""


# =============================================== Imports ===============================================
import os
from PIL import ImageDraw, ImageFont
from PIL.Image import Image
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from enum import Enum
from pathlib import Path

# ================================================ Utils ================================================
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

type Dimension = tuple[PositiveNotZeroInt, PositiveNotZeroInt]


# ============================================== Functions ==============================================
def img_to_ascii(
        img : Path | Image,
        ascii_gradient : AsciiGradient = AsciiGradient.LEVEL_10,
        output_dimensions : Dimension | Percent = Dimension(50, 50),
        outpout_file : Path = None,
        space : PositiveInt = 0,
        multi_thread : bool = True
    )-> str:
    """
    Converts an image to ASCII art and optionally writes it to a file and returns it as a string.

    Parameters:
        img (Path | Image): The path to the input image file or the image object itself.
        ascii_gradient (AsciiGradient, optional): The ASCII gradient to use. Defaults to AsciiGradient.LEVEL_10.
        output_dimensions (Dimension | Percent, optional): The dimensions of the output image. If a float, it is interpreted as a percentage of the input image dimensions. Defaults to Dimension(50, 50).
        outpout_file (Path, optional): The path to the output text file if outpout_in_file is True. Defaults to None.
        space (PositiveInt, optional): The number of spaces to add between ASCII characters. Defaults to 0.
        multi_thread (bool, optional): Whether to use multi-threading or not. Defaults to True.

    Returns:
        str: The ASCII art as a string.
    """
    # Check input types and values
    if isinstance(img, (str, Path)):
        img = Image.open(Path(img))
    if outpout_file is not None:
        outpout_file = Path(outpout_file)
    if not isinstance(ascii_gradient, AsciiGradient):
        raise TypeError(f'Expected an AsciiGradient, got {type(ascii_gradient)}.')
    
    if isinstance(output_dimensions, float):
        output_dimensions = (int(img.width*output_dimensions), int(img.height*output_dimensions))
    else:
        output_dimensions = Dimension(*output_dimensions)
    space = PositiveInt(space)
    
    # Resize the image
    img = img.resize(output_dimensions)

    # Create the ascii image
    def line_process(img : Image, y : int)-> str :
        return ''.join(
            (ascii_gradient.value[(sum(img.getpixel((x, y))) // len(img.getpixel((x, y)))) * (len(ascii_gradient.value) - 1) // 255] +''*space
            for x in range(img.width)))
    
    if multi_thread :
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(line_process, img,y)for y in range(img.height)]
            ascii_art = '\n'.join(futur.result() for futur in futures)
    else:
        ascii_art = '\n'.join(line_process(img,y)for y in range(img.height))
    
    # Write the ascii art to a file
    if outpout_file is not None:
        with open(outpout_file, 'w') as f:
            f.write(ascii_art)
    
    return ascii_art

def process_images(images_files):
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(img_to_ascii, image_file) for image_file in images_files]
        return [future.result()for future in futures]

def ascii_to_img(
        ascii_art : str, outpout_file : str = 'ascii_art.png', text_color : tuple[int,int,int] | str = (100, 255, 100), bg_color : tuple[int,int,int] | str = (0, 0, 0), compression : int = 5, font_file : str = 'font/MonospaceTypewriter.ttf', font_size : float = 1.0)-> Image | None :
    """
    Converts an ASCII Art string into an image and saves it to a file.
    """
    try :
        lines = ascii_art.split('\n')
        img = Image.new('RGB', (max([len(line) for line in lines])*compression,len(lines)*compression), color = bg_color)
        drawer = ImageDraw.Draw(img)
        for y, line in enumerate(lines) :
            for x, char in enumerate(line) :
                drawer.text((x*compression, y*compression), char, font=ImageFont.truetype(font_file, int(font_size*compression)), fill=text_color)
        img.save(outpout_file)
        return img
    except Exception as e :
        e.with_traceback()
        print(f'caught {type(e)}: {e}')
        return None

def process_ascii_art(ascii_arts, outputs_files):
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(ascii_to_img, ascii_art, output_file) for ascii_art, output_file in zip(ascii_arts, outputs_files)]
        return [future.result()for future in futures]

def ascii_to_greyimg(ascii_art : str, outpout_file : str = 'ascii_art.png', text_color : tuple[int,int,int] | str = (100, 255, 100), bg_color : tuple[int,int,int] | str = (0, 0, 0), compression : int = 5, font_file : str = 'font/MonospaceTypewriter.ttf', font_size : float = 1.0)-> Image | None :
    raise NotImplementedError("This function is not yet implemented.")