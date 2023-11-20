_For version 3.27 and beyond ..._
# ascii_images
A Python project that converts images into ASCII art.

## More details
This project add just two functions :
- The ``image_to_ascii`` function takes an image file as input and converts it into ASCII art. The ASCII art can be optionally written to a specified output file and returned as a string. The image can be resized based on the provided parameters, and the grayscale level and the ASCII characters for the ASCII art can be selected. The function returns None if an error occurs during the process. The function prints the exception and its traceback if an error occurs. Please note that this function requires the PIL (Pillow) library for opening and manipulating the image.
- The ``ascii_to_image`` function is designed to convert an ASCII Art string into an image and save it to a file. The function works by creating a new image with the specified background color and dimensions based on the ASCII art string. It then draws each character of the ASCII art onto the image using the specified text color and font. If the image is successfully created and saved, it is returned by the function; otherwise, if an exception occurs, the function prints the exception and returns None.

## Installation
To install this project, you need to have Python 3 and the following libraries:

- Pillow

You can install them using pip:

```bash
pip install Pillow
```

## Usage
To use this project, you need to have some images. Then, you can run the `imgTOascii.py.py` file with the following methods:

Run python if you will run my project in a terminal :
```bash
python
```
Then use my project as an import in your code :
```python
import imgTOascii
```
Finally, call the function(s) in your code as follows (here the arguments are just for the exemple):
```python
ascii_art : str = imgTOascii.image_to_ascii("images/1.jpg", resize = True, resize_percentage = 0.1, nb_space = 1, gscale = 1)
ascii_art : str = imgTOascii.image_to_ascii("images/1.jpg", resize = None, xsize = 30, ysize = 30, nb_space = 0)
```

```python
import PIL
ascii_art = """
  _____
 /     \\
| () () |
 \\  ^  /
  |||||
"""
image : PIL.Image = ascii_to_image(ascii_art)
image : PIL.Image = ascii_to_image(ascii_art, output_file='my_ascii_art.png', text_color='white', bg_color='black')
image : PIL.Image = ascii_to_image(ascii_art, output_file='my_ascii_art.png', text_color=(255, 0, 255), bg_color=(0, 255, 0), compression=10, font_file='my_font.ttf', font_size=1.5)

```

This will create ASCII art versions of the images in the `output` (`out.txt` by default) file. You can adjust the parameters the `image_to_ascii` function to change the size and contrast of the ASCII art.

## Example
Here is an example of an input image and its ASCII art output:

Commands :
```python
import imgTOascii
imgTOascii.ascii_to_image(imgTOascii.image_to_ascii("logo.ico", resize = True, resize_percentage = 0.5, nb_space = 0, gscale = 0),'Capture.png',bg_color='black',text_color='white')
```

![Input image](/logo.ico)
![Output image](/Capture.png)

## License
This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.
