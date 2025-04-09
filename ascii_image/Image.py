"""
This module provides functions to represent an image as ASCII art or reverse.
"""


# =============================================== Imports ===============================================
import os
from PIL import ImageDraw, ImageFont
from PIL.Image import Image
from concurrent.futures import ThreadPoolExecutor


# ============================================== Functions ==============================================
def img_to_ascii(
        input : str | Image,
        outpout_in_file : bool = True,
        outpout_file : str = 'out.txt',
        resize : bool = False,
        resize_percentage : float = 0.5,
        xsize : int = 50,
        ysize : int = 50,
        gscale : int = 0,
        nb_space : int = 0,
        other_ascii_gradient : str = None
    )-> str | None :
    """
    Converts an image to ASCII art and optionally writes it to a file and returns it as a string.

    Parameters:
        input (str | Image): The path to the input image file or.
        outpout_in_file (bool, optional): Whether to write the ASCII art to a file or not. Defaults to True.
        outpout_file (str, optional): The path to the output text file if outpout_in_file is True. Defaults to 'out.txt'.
        resize (bool, optional): Whether to resize the image or not. If False, the image is not resized. If True, the image is resized by resize_percentage. Defaults to False.
        resize_percentage (float, optional): The percentage to resize the image by if resize is True. Must be between 0 and 1. Defaults to 0.5.
        xsize (int, optional): The width to resize the image to if resize is None. Defaults to 50.
        ysize (int, optional): The height to resize the image to if resize is None. Defaults to 50.
        gscale (int, optional): The grayscale level to use for the ASCII art. 0 for 10 levels of gray, 1 for ~70 levels of gray. Defaults to 0.
        nb_space (int, optional): The number of spaces to add between ASCII characters. Defaults to 0.
        other_ascii_gradient (str, optional): A custom string of ASCII characters to use for the ASCII art. If None, the default gradients are used. Defaults to None.

    Returns:
        str: The ASCII art as a string, or None if an error occurred.
    """
    try :
        ascii_char = [' .:-=+*#%@',''' ."`^",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'''][gscale] if other_ascii_gradient == None else other_ascii_gradient #10 levels of gray then ~70 levels of gray or a personalized one
        def to_ascii(image : Image):
            if resize == None :
                image = image.resize((xsize, ysize))
            elif resize :
                image = image.resize((int(resize_percentage*image.width), int(resize_percentage*image.height)))
            # Create the ascii image
            def line_process(image : Image, y : int)-> str :
                return ''.join(
                    (ascii_char[(sum(image.getpixel((x, y))) // len(image.getpixel((x, y)))) * (len(ascii_char) - 1) // 255] + ' '*nb_space
                    for x in range(image.width)))
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(line_process(image,y))for y in range(image.height)]
                return '\n'.join(futur.result() for futur in futures)
        if type(input) == str :
            with Image.open(input) as image : ascii_art = to_ascii(image)
        else :
            ascii_art = to_ascii(input)
        if outpout_in_file :
            with open(outpout_file,'w') as image : image.write(ascii_art)
        return ascii_art
    except Exception as e:
        e.with_traceback()
        print(f'caught {type(e)}: {e}')
        return None

def process_images(images_files):
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(img_to_ascii, image_file) for image_file in images_files]
        return [future.result()for future in futures]

def ascii_to_img(
        ascii_art : str, outpout_file : str = 'ascii_art.png', text_color : tuple[int,int,int] | str = (100, 255, 100), bg_color : tuple[int,int,int] | str = (0, 0, 0), compression : int = 5, font_file : str = 'font/MonospaceTypewriter.ttf', font_size : float = 1.0)-> Image | None :
    """
    Converts an ASCII Art string into an image and saves it to a file.

    Parameters:
        ascii_art (str): The ASCII Art string to be converted to an image.
        outpout_file (str, optional): The file path where the image will be saved. By default, 'ascii_art.png'.
        text_color (tuple[int,int,int] | str, optional) : Text color in RGB or color name. Default: (100, 255, 100).
        bg_color (tuple[int,int,int] | str, optional): Background color in RGB or color name. Default: (0, 0, 0).
        compression (int, optional): Image compression factor. Default is 5.
        font_file (str, optional): The file path of the font to be used. Default: 'font/MonospaceTypewriter.ttf'.
        font_size (float, optional): The font size. Defaults to 1.0.

    Returns :
        Image: the image if it has been created and saved successfully, None otherwise.
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