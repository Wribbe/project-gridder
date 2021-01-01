import itertools
import sys

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

A4 = (210, 297) # mm.
printer_resolution = 300
printer_pixels = (printer_resolution*r for r in A4)

num_lines = (20, 20)

def guides():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    iteration = -1
    while True:
        for c in alphabet:
            prefix = ""
            if iteration >= 0:
                prefix += alphabet[iteration].upper()
            yield f"{prefix}{c.upper()}"
        iteration += 1


def run():

    name, *args = sys.argv
    if not args:
        print(f"[Usage:] {name} PATH_IMAGE")
        return
    path_image = Path(args[0])
    if not path_image.is_file():
        print(f"No such file: {path_image}, aborting.")
        return

    image = Image.open(str(path_image))

    width_line = 3
    end_x, end_y = (i-width_line/2 for i in image.size)
    delta_x = end_x/num_lines[0]
    delta_y = end_y/num_lines[1]

    border = int(min([delta_y, delta_x]))

    draw = ImageDraw.Draw(image)
    x, y = (0, 0)

    while x <= end_x:
        draw.line((x, 0, x, end_y), fill=0, width=width_line)
        x += delta_x
    while y <= end_y:
        draw.line((0, y, end_x, y), fill=0, width=width_line)
        y += delta_y

    # Add border.
    image_new = Image.new(
        "RGB", tuple(d+border*2 for d in image.size), color=(255,255,255)
    )
    image_new.paste(image, (border, border))

    # Prepare for guides.
    draw = ImageDraw.Draw(image_new)
    font = ImageFont.truetype('OpenSans-Regular.ttf', size=int(border*0.6))

    # Add horizontal
    pos_top = border+delta_x/2
    offset_y = delta_y*num_lines[1]+border
    for _, g in zip(range(num_lines[0]), guides()):
        draw.text((pos_top, border/2), g, fill=0, font=font, anchor="mm")
        draw.text((pos_top, border/2+offset_y), g, fill=0, font=font, anchor="mm")
        pos_top += delta_x

    pos_side = border+delta_y/2
    offset_x = delta_x*num_lines[0]+border
    for _, g in zip(range(num_lines[1]), guides()):
        draw.text((border/2, pos_side), g, fill=0, font=font, anchor="mm")
        draw.text((border/2+offset_x, pos_side), g, fill=0, font=font, anchor="mm")
        pos_side += delta_y

#    delta_x, delta_y = [int(a/b) for a,b in zip(image.size, num_lines)]
#    image_x, image_y = image.size
#    xs = list(range(image_x+3)[::delta_x])
#    ys = list(range(image_y+3)[::delta_y])
#    xs[-1] -= 3
#    ys[-1] -= 3
#
#    print(image.size)
#    print(list(xs))
#    print(list(ys))
#
#    draw = ImageDraw.Draw(image)
#    for x in xs:
#        draw.line((x, 0, x, image_y), fill=0, width=3)
#    for y in ys:
#        draw.line((0, y, image_x, y), fill=0, width=3)
#
##    draw.line((0, 0) + image.size, fill=(255,255,255,125), width=20)
##    draw.line((0, image.size[1], image.size[0], 0), fill=255, width=20)
    image_new.save("test.png", "PNG")

