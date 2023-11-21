# =============================================== Imports ===============================================
import numpy
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip

# ================================================ Init =================================================
VERSION = 4.0
NAME = __file__

# ============================================== Functions ==============================================

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: IMAGE ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def image_to_ascii(input : str | Image.Image, outpout_in_file : bool = True, outpout_file : str = 'out.txt', resize : bool = False, resize_percentage : float = 0.5, xsize : int = 50, ysize : int = 50, gscale : int = 0, nb_space : int = 0, other_ascii_gradient : str = None)-> str :
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
        def to_ascii(image : Image.Image):
            if resize == None :
                image = image.resize((xsize, ysize))
            elif resize :
                image = image.resize((int(resize_percentage*image.width), int(resize_percentage*image.height)))
            # Create the ascii image
            return (''.join(''.join((ascii_char[(sum(image.getpixel((x, y))) // len(image.getpixel((x, y)))) * (len(ascii_char) - 1) // 255] + ' '*nb_space for x in range(image.width))) + '\n' for y in range(image.height)))[:-1]
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

def ascii_to_image(ascii_art : str, outpout_file : str = 'ascii_art.png', text_color : tuple[int,int,int] | str = (100, 255, 100), bg_color : tuple[int,int,int] | str = (0, 0, 0), compression : int = 5, font_file : str = 'font/MonospaceTypewriter.ttf', font_size : float = 1.0)-> Image.Image :
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

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: VIDEO ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def video_to_ascii(input_file : str, outpout_in_file : bool = True, outpout_file : str = 'out.txt', resize : bool = False, resize_percentage : float = 0.5, xsize : int = 50, ysize : int = 50, gscale : int = 0, nb_space : int = 0, other_ascii_gradient : str = None)-> tuple[list[str], int, AudioFileClip] :
    """
    Converts video to ASCII art.

    Args:
        input_file (str): Path to video file to be converted.
        outpout_in_file (bool, optional): If True, saves ASCII art to file. Defaults to True.
        outpout_file (str, optional): Path to output file. Defaults to 'out.txt'.
        resize (bool, optional): If True, resizes image before conversion. Defaults to False.
        resize_percentage (float, optional): Resize percentage. Defaults to 0.5.
        xsize (int, optional): Width of resized image. Defaults to 50.
        ysize (int, optional): Height of resized image. Defaults to 50.
        gscale (int, optional): Gray scale for conversion to ASCII. Defaults to 0.
        nb_space (int, optional): Number of spaces to add between ASCII characters. Defaults to 0.
        other_ascii_gradient (str, optional): Other ASCII gradient to be used for conversion. Defaults to None.

    Returns:
        tuple: A tuple containing a list of ASCII strings, the video's frame rate and the video's audio.
    """
    try :
        with VideoFileClip(input_file) as video:
            tmp = ([image_to_ascii(Image.fromarray(frame), outpout_in_file = False, outpout_file = outpout_file, resize = resize, resize_percentage = resize_percentage, xsize = xsize, ysize = ysize, gscale = gscale, nb_space = nb_space, other_ascii_gradient = other_ascii_gradient) for frame in video.iter_frames()],video.fps,video.audio)
        if outpout_in_file :
            with open(outpout_file,'w') as image : image.write(tmp[0])
        return tmp
    except Exception as e:
        e.with_traceback()
        print(f'caught {type(e)}: {e}')
        return None

def ascii_to_video(ascii_art : list[str], fps : int, outpout_in_file : bool = False, outpout_file : str = 'ascii_art.mp4', text_color : tuple[int,int,int] | str = (100, 255, 100), bg_color : tuple[int,int,int] | str = (0, 0, 0), compression : int = 5, font_file : str = 'font/MonospaceTypewriter.ttf', font_size : float = 1.0, audio : AudioFileClip = None)-> Image :
    """
    Converts ASCII art to video.

    Args:
        ascii_art (list[str]): List of ASCII strings to convert to video.
        fps (int): Number of frames per second for video.
        outpout_in_file (bool, optional): If True, saves video to file. Defaults to False.
        outpout_file (str, optional): Path to output file. Defaults to 'ascii_art.mp4'.
        text_color (tuple[int,int,int] | str, optional): Text color in RGB or color name. Defaults to (100, 255, 100).
        bg_color (tuple[int,int,int] | str, optional): Background color in RGB or color name. Defaults to (0, 0, 0).
        compression (int, optional): Compression factor for video. Defaults to 5.
        font_file (str, optional): Path to font file to be used for text. Defaults to 'font/MonospaceTypewriter.ttf'.
        font_size (float, optional): Font size. Defaults to 1.0.
        audio (AudioFileClip, optional): Audio to add to video. Defaults to None.

    Returns:
        Image: An Image object representing the created video.
    """
    try :
        max_width = max([len(line) for frame in ascii_art for line in frame.split('\n')])
        max_height = max([len(frame.split('\n')) for frame in ascii_art])
        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        frames = []
        for frame in ascii_art :
            img = Image.new('RGB', (max_width*compression,max_height*compression), color = bg_color)
            for y, line in enumerate(frame.split('\n')) :
                for x, char in enumerate(line) :
                    (ImageDraw.Draw(img)).text((x*compression, y*compression), char, font=ImageFont.truetype(font_file, int(font_size*compression)), fill=text_color)
            frames.append(img)
        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        video_clip = ImageSequenceClip([numpy.array(image) for image in frames], fps=fps)
        if audio != None : video_clip.set_audio(audio)
        if outpout_in_file : video_clip.write_videofile(outpout_file)
        return video_clip
    except Exception as e :
        e.with_traceback()
        print(f'caught {type(e)}: {e}')
        return None