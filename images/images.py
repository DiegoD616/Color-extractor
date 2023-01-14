from PIL import Image, ImageDraw, ImageFont
import numpy as np

def load_image_as_array(filename: str, resize: tuple = None, color_mode: str = "RGB") -> np.array:
    """Recives a path to an image and returns the image as a numpy.array

    Args:
        filename (str): 
            The path to the image file to load.
        resize (tuple, optional): 
            A tuple with dimentions for the loaded image. 
            If none the images origan dimentions will be taken. Defaults to None.
        color_mode (str, optional): 
            String for the image's colors. As taken by the pillow lib.
            Defaults to "RGB".

    Returns:
        numpy.array: The loaded image as a numpy array.
    """

    img = Image.open(filename).convert(color_mode)
    if resize is not None: img = img.resize(resize)
    return np.array(img).astype("float32")

def rendered_img(img, color_pallet):
    """Renders an image with the color_pallet next to the img.

    Args:
        img (numpy.array): An image as a numpy array.
        color_pallet (numpy.array): A color pallet as a 2D numpy.array.

    Returns:
        pillow.image: A pillow.image object with the color pallet rendered.
    """

    result = get_canvas_result(img)
    drawable = ImageDraw.Draw(result)
    drawable.text((10, 10), "Paleta de colores", size=250, fill="black")
    add_color_pallet(drawable, color_pallet)
    return result

def get_canvas_result(img):
    """Creates a canvas e.i a drawable image with img pasted to the right of the canvas.

    Args:
        img (numpy.array): An image as a numpy array.

    Returns:
        pillow.image: A pillow image with whitespace and the origial image.
    """

    image = Image.fromarray(np.uint8(img))
    width, height = image.size
    new_width = width + width//4; new_height = height
    result = Image.new(image.mode, (new_width, new_height), (255, 255, 255))
    result.paste(image, (width//4, 0))
    return result

def add_color_pallet(draw, color_pallet):
    """Recives a drawable image and a color pallet to be rendered in the image.

    Args:
        draw (pillow.image): The image where the color_pallet will be draw
        color_pallet (numpy.array): The color pallet to be draw
    """

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

def rgb_to_hex(rgb): 
    """Takes an RGB color and returns a string with it's hex code.

    Args:
        rgb (tuple(int, int, int)): The RGB color

    Returns:
        str: The hex code for the RGB color
    """
    return "#{:02X}{:02X}{:02X}".format(*rgb)