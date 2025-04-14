"""
This module provides functions to convert an image into ASCII art.
"""

# =============================================== Imports ===============================================
import numpy as np
from enum import Enum
from pathlib import Path
from PIL import ImageDraw, ImageFont
from PIL.Image import Image, open as open_image, new as new_image, fromarray

from .types import Dimension, GrayScale, PositiveInt, ProcessType
from .color import Color, ColorLevel, BLACK
from .image import image_to_grayscale


# =============================================== Objects ===============================================
class AsciiGradient(str):
    """
    A string that represents an ASCII gradient.
    """
    def __new__(cls, value):
        cls.validate(value)
        return str.__new__(cls, value)
    
    @staticmethod
    def validate(gradient: str) -> None:
        """
        Validate an ASCII gradient string.

        Parameters:
            gradient (str): The ASCII gradient string to validate.

        Returns:
            bool: True if the gradient is valid, False otherwise.
        """
        if not isinstance(gradient, str):
            raise TypeError(f'Expected a string, got {type(gradient)}.')
        if len(gradient) < 2:
            raise ValueError(f'Expected a string with at least 2 characters, got {len(gradient)}.')
        if len(set(gradient)) != len(gradient):
            raise ValueError(f'Expected a string with unique characters, got {gradient}.')
    
    @staticmethod
    def is_gradient(gradient: str) -> bool:
        """
        Validate an ASCII gradient string.

        Parameters:
            gradient (str): The ASCII gradient string to validate.

        Returns:
            bool: True if the gradient is valid, False otherwise.
        """
        try:
            AsciiGradient.validate(gradient)
            return True
        except TypeError|ValueError: return False


class AsciiGradientBaseList(Enum):
    """
    Enum class for the different gradients to use for the ASCII art.
    """
    LEVEL_10 = ' .:-=+*#%@'
    LEVEL_67 = ' ."`^",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
    LEVEL_70 = """ .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"""
    LEVEL_92 = """ `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"""

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


class AsciiArt(str):
    """
    A string that represents an ASCII art image.
    """
    def __new__(cls, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected a string, got {type(value)}.')
        return str.__new__(cls, value)

    @property
    def width(self):
        """
        Get the width of the ASCII art.
        """
        return max(len(line) for line in self.split('\n'))

    @property
    def height(self):
        """
        Get the height of the ASCII art.
        """
        return len(self.split('\n'))
    
    @property
    def size(self):
        """
        Get the size of the ASCII art as a Dimension object.
        """
        return Dimension(self.width, self.height)
    
    @property
    def gradient(self) -> AsciiGradient:
        """
        Get the ASCII art gradient.
        """
        return self.gradient
    
    @gradient.setter
    def gradient(self, gradient: AsciiGradient):
        """
        Set the ASCII art gradient.
        """
        self.gradient = AsciiGradient(gradient)
    
    
    def guess_ascii_gradient(self) -> AsciiGradient:
        index = {c: i for i, c in enumerate(AsciiGradientBaseList.LEVEL_92.value)}
        return AsciiGradient(''.join(sorted(set(self), key=lambda x: index[x])))
    

    def save(self, output_file: Path | str) -> None:
        """
        Save the ASCII art to a file.

        Parameters:
            output_file (Path | str): The path to the output file.
        """
        with open(output_file, 'w') as f:
            f.write(self)
    

    def to_grayscale(self, gradient: AsciiGradient=None) -> GrayScale:
        """
        Convert the ASCII art to a greyscale numpy array.

        Parameters:
            gradient (AsciiGradient, optional): The ASCII gradient to use. Defaults to AsciiGradient.LEVEL_10.

        Returns:
            GrayScale: The greyscale numpy array.
        """
        n = 255 / (len(gradient) - 1)
        indexed_gradient = {c:i for i,c in enumerate(gradient)}

        lines = self.split('\n')
        arr = np.zeros((len(lines), max(len(line) for line in lines)), dtype=ColorLevel)

        for y, line in enumerate(lines) :
            for x, char in enumerate(line) :
                arr[y,x] = indexed_gradient[char]*n
        return arr


    @classmethod
    def from_grayscale(
        cls,
        grayscale: GrayScale,
        gradient: AsciiGradient,
        space : PositiveInt = 0
    ) -> 'AsciiArt':
        """
        Convert a greyscale numpy array to an ASCII art string.

        Parameters:
            grayscale (GrayScale):          The greyscale numpy array to convert.
            gradient (AsciiGradient):       The ASCII gradient to use.
            space (PositiveInt, optional):  The number of spaces to add between ASCII characters. Defaults to 0.

        Returns:
            AsciiArt: The ASCII art string.
        """
        gradient = AsciiGradient(gradient)

        # Normalize to ASCII gradient indices
        n = (len(gradient) - 1) / 255
        scaled = (grayscale * n).astype(ColorLevel)

        # Map values to ASCII characters
        chars = np.array(list(gradient))[scaled]

        if space > 0: chars = np.char.add(chars, ' ' * space)

        # Join rows
        return cls('\n'.join(''.join(row) for row in chars))


    @classmethod
    def from_image(
        cls,
        img: Path | Image,
        gradient: AsciiGradient = None,
        space : PositiveInt = 0,
        grayscale_mode : ProcessType = ProcessType.AVG
    ) -> 'AsciiArt':    
        """
        Convert an image to an ASCII art string.

        Parameters:
            img (Path | Image):            The path to the image file or the image object to convert.
            gradient (AsciiGradient, optional): The ASCII gradient to use. Defaults to None.
            space (PositiveInt, optional):  The number of spaces to add between ASCII characters. Defaults to 0.
            grayscale_mode (ProcessType, optional): The method to use to convert the image to grayscale. Defaults to ProcessType.AVG.
            
        Returns:
            AsciiArt: The ASCII art string.
        """
        # Check input types and values
        img_must_be_closed = False
        if isinstance(img, (str, Path)): img, img_must_be_closed = open_image(Path(img)), True
        if not isinstance(gradient, AsciiGradient): raise TypeError(f'Expected an AsciiGradient, got {type(ascii_gradient)}.')
        output_dimensions = (int(img.width * output_dimensions), int(img.height * output_dimensions)) if isinstance(output_dimensions, float) else Dimension(*output_dimensions)
        space = PositiveInt(space)

        # Convert to ASCII art
        ascii_art = cls.from_grayscale(
            # Compute grayscale
            grayscale=image_to_grayscale(
                img.resize(output_dimensions),
                grayscale_mode
            ),
            ascii_gradient=gradient,
            space=space
        )
        if img_must_be_closed: img.close()
        return ascii_art
    

    def to_graylevel_img(self) -> Image:
        """
        Convert the ASCII art to a grayscale image.
        """
        return fromarray(self.to_grayscale().astype(np.uint8), mode='L')
    

    def to_image_of_ascii(
        self,
        font_file : str,
        font_size : float = 1.0,
        text_color : Color = Color(100, 255, 100),
        bg_color : Color = BLACK,
        compression : PositiveInt = 5,
    )-> Image :
        """
        Converts an ASCII Art string into an image and saves it to a file.

        Parameters:
            font_file (str, optional):                  The path to the font file to use.
            font_size (float, optional):                The font size to use. Defaults to 1.0.
            text_color (Color, optional):               The color of the text. Defaults to Color(100, 255, 100) (a light green).
            bg_color (Color, optional):                 The color of the background. Defaults to Black.
            compression (int, optional):                The compression factor to use. Defaults to 5.
            output_file (str | Path, optional):         The path to the output file. Defaults to 'ascii_art.png'.

        Returns:
            Image: The output image object.
        """
        lines = self.split('\n')
        img = new_image(
            mode='RGB',
            size=(
                max(len(line) for line in lines)*compression,
                len(lines)*compression
            ),
            color = bg_color
        )
        drawer = ImageDraw.Draw(img)
        for y, line in enumerate(lines) :
            for x, char in enumerate(line) :
                drawer.text(
                    xy=(x*compression, y*compression),
                    text=char,
                    font=ImageFont.truetype(font_file, int(font_size*compression)),
                    fill=text_color
                )
        return img

        
def guess_ascii_gradient_by_most_common(ascii_art: str) -> str:
    """
    Guess the ASCII art gradient based on the most common characters.

    Parameters:
        ascii_art (str): The ASCII art string to guess the gradient for.

    Returns:
        str: The ASCII art gradient.
    """
    # Count the number of occurrences of each character in the ASCII art
    counts = {}
    for char in ascii_art:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1

    # Find the character with the highest count
    max_count = 0
    max_char = None
    for char, count in counts.items():
        if count > max_count:
            max_count = count
            max_char = char

    # Guess the gradient based on the most common character
    match max_char:
        case  ' ': return AsciiGradientBaseList.LEVEL_10.value
        case  '.': return AsciiGradientBaseList.LEVEL_67.value
        case  ',': return AsciiGradientBaseList.LEVEL_70.value
        case  '`': return AsciiGradientBaseList.LEVEL_92.value
        case _: raise ValueError(f'Could not guess the ASCII art gradient for character {max_char}.')