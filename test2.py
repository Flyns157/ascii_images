from PIL import Image

def image_to_ascii_art(input_file : str, outpout_file : str = 'out.txt', resize : bool = True, xsize : int = 50, ysize : int = 50, gscale : int = 0, nb_space : int = 1)-> bool :
    try :
        # Clear output file
        tmp = open(outpout_file,'w')
        tmp.write('')
        tmp.close()
        # Create the output
        file = open(outpout_file,'a')
        ascii_char = [' .:-=+*#%@',''' ."`^",:;Il!i~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'''][gscale] #10 levels of gray then ~70 levels of gray
        with Image.open(input_file) as image:
            if resize :
                image = image.resize((xsize, ysize))
            # Create the ascii image
            file.write(''.join(''.join((ascii_char[(sum(image.getpixel((x, y))) // len(image.getpixel((x, y)))) * (len(ascii_char) - 1) // 255] + ' '*nb_space for x in range(image.width))) + '\n' for y in range(image.height)))
    except Exception as e:
        print(f'caught {type(e)}: {e}')
    finally :
        try :
            file.close()
        except Exception :
            pass

image_to_ascii_art("28335962_2173261412901459_3993534359767236958_o.jpg",)