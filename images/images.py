from PIL import Image, ImageDraw, ImageFont
import numpy as np

def load_image_as_array(filename, resize=None, color_mode = "RGB"):
    img = Image.open(filename).convert(color_mode)
    if resize is not None: img = img.resize(resize)
    return np.array(img).astype("float32")

def save_image(img, color_pallet, name):
    result = get_canvas_result(img)
    drawable = ImageDraw.Draw(result)
    drawable.text((10, 10), "Paleta de colores", size=250, fill="black")
    add_color_pallet(drawable, color_pallet)
    result.save(name)

def get_canvas_result(img):
    image = Image.fromarray(np.uint8(img))
    width, height = image.size
    new_width = width + width//4; new_height = height
    result = Image.new(image.mode, (new_width, new_height), (255, 255, 255))
    result.paste(image, (width//4, 0))
    return result

def add_color_pallet(draw, color_pallet):
    color_square_size       = 60
    color_square_size_begin = 50
    color_square_size_end   = color_square_size_begin + color_square_size
    for color_idx, color in enumerate(color_pallet):
        draw.rectangle(
            (20, color_square_size_begin) + (20 + color_square_size, color_square_size_end), 
            fill=tuple(color)
        )
        draw.text(
            (20+color_square_size+20, color_square_size_begin + color_square_size//2), 
            rgb_to_hex(tuple(color)), 
            size=350, fill="black"
        )
        
        color_square_size_begin += color_square_size
        color_square_size_end   = color_square_size_begin + color_square_size

def rgb_to_hex(rgb): return "#{:02X}{:02X}{:02X}".format(*rgb)