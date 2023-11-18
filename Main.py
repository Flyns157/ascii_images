# =============================================== Imports ===============================================
from PIL import Image

# ================================================ Init =================================================
VERSION = 2.0
NAME = __file__

# ============================================== Functions ==============================================
def image_to_ascii_art(input_file : str, outpout_file : str = 'out.txt', resize : bool = False, resize_percentage : float = 0.5, xsize : int = 50, ysize : int = 50, gscale : int = 0, nb_space : int = 1)-> bool :
    """
    Converts an image to ASCII art and writes it to a file.

    Parameters:
        input_file (str): The path to the input image file.
        outpout_file (str, optional): The path to the output text file. Defaults to 'out.txt'.
        resize (bool, optional): Whether to resize the image or not. If None, the image is resized to (xsize, ysize). If True, the image is resized by resize_percentage. Defaults to None.
        resize_percentage (float, optional): The percentage to resize the image by if resize is True. Defaults to 50.
        xsize (int, optional): The width to resize the image to if resize is None. Defaults to 50.
        ysize (int, optional): The height to resize the image to if resize is None. Defaults to 50.
        gscale (int, optional): The grayscale level to use for the ASCII art. 0 for 10 levels of gray, 1 for ~70 levels of gray. Defaults to 0.
        nb_space (int, optional): The number of spaces to add between ASCII characters. Defaults to 1.

    Returns:
        bool: True if the ASCII art was successfully written to the file, False otherwise.
    """
    try :
        # Clear output file
        tmp = open(outpout_file,'w')
        tmp.write('')
        tmp.close()
        # Create the output
        file = open(outpout_file,'a')
        ascii_char = [' .:-=+*#%@',''' ."`^",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'''][gscale] #10 levels of gray then ~70 levels of gray
        with Image.open(input_file) as image:
            if resize == None :
                image = image.resize((xsize, ysize))
            elif resize :
                image = image.resize((int(resize_percentage*image.width), int(resize_percentage*image.height)))
            # Create the ascii image
            file.write(''.join(''.join((ascii_char[(sum(image.getpixel((x, y))) // len(image.getpixel((x, y)))) * (len(ascii_char) - 1) // 255] + ' '*nb_space for x in range(image.width))) + '\n' for y in range(image.height)))
    except Exception as e:
        print(f'caught {type(e)}: {e}')
    finally :
        try :
            file.close()
        except Exception :
            pass

# ================================================= Run =================================================
image_to_ascii_art("images/1.jpg", resize = True, resize_percentage = 0.1, nb_space = 1, gscale = 0)