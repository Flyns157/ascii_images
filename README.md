_For version 2.1 and beyond ..._
# ascii_images
A Python project that converts images into ASCII art.

## More details
This project add just on function what takes an image file as input and converts it into ASCII art. The ASCII art can be optionally written to a specified output file and returned as a string. The image can be resized based on the provided parameters, and the grayscale level and the ASCII characters for the ASCII art can be selected. The function returns None if an error occurs during the process. The function prints the exception and its traceback if an error occurs. The output file is always closed before the function returns, even if an error occurs. Please note that this function requires the PIL (Pillow) library for opening and manipulating the image.

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
Finally, call the image_to_ascii function in your code as follows (here the arguments are just for the exemple):
```python
imgTOascii.image_to_ascii("images/1.jpg", resize = True, resize_percentage = 0.1, nb_space = 1, gscale = 1)
imgTOascii.image_to_ascii("images/1.jpg", resize = None, xsize = 30, ysize = 30, nb_space = 0)
```

This will create ASCII art versions of the images in the `output` (`out.txt` by default) file. You can adjust the parameters the `image_to_ascii` function to change the size and contrast of the ASCII art.

## Example
Here is an example of an input image and its ASCII art output:

(command : ``imgTOascii.image_to_ascii("logo.ico", resize = True, resize_percentage = 0.5, nb_space = 1, gscale = 0)``)

![Input image](/logo.ico)
![Output image](/Capture.png)

## License
This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.
