# =============================================== Imports ===============================================
from PIL import Image

# ================================================ Init =================================================
VERSION = 1.0
# Cleaning output file
tmp = open('out.txt','w')
tmp.write('')
tmp.close()
# Some initializations
file = open('out.txt','a')
size = 100
# gradations from darkest to lightest
gscale1 = ' .:-=+*#%@' # 10 levels of gray
gscale2 = ''' ."`^",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$''' #~70 levels of gray
ascii_char = gscale1

# =============================================== Program ===============================================
with Image.open("logo.ico") as image:
    image = image.resize((size, size))

    for y in range(image.height):
        line = ""
        for x in range(image.width):
            line += ascii_char[(sum(image.getpixel((x, y))) // len(image.getpixel((x, y)))) * (len(ascii_char) - 1) // 255] + ' '
        file.write(line + '\n')

# =============================================== closing ===============================================
file.close()