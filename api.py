import aiofiles
import asyncio
import io
import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, StreamingResponse

from color_extractor import ColorExtractor
from images import load_image_as_array
from PIL import Image

ITERS_TO_RUN = 5
SIZE_FOR_LOADED_IMGS = (685, 385)
DIR_IMGS_TO_PROCESS = "./base_imgs/"

app = FastAPI()

@app.post("/single-pallet")
def single_pallet( amount_colors: int, image_to_process: UploadFile = File(...) ) -> dict:
    """Returns a dictionary with the image's most relevant colors as the values and integers as the keys.
    The color will be returned in RGB format.

    Args:
        amount_colors (int): The amount of colors to extract from image_to_process
        image_to_process (UploadFile): This is the image from which the colors will be extracted.

    Returns:
        dict: A dictionary with the most relevant colors
    """

    destination_file_path = asyncio.run(save_recived_file(image_to_process))
    loaded_img = load_image_as_array(destination_file_path, resize = SIZE_FOR_LOADED_IMGS)
    color_extractor = ColorExtractor(amount_colors, ITERS_TO_RUN, SIZE_FOR_LOADED_IMGS)
    color_pallet = color_extractor.get_color_pallet(loaded_img)
    os.remove(destination_file_path)
    return color_pallet_to_dic(color_pallet)

def color_pallet_to_dic(color_pallet: numpy.array) -> dict:
    """Transforms the color pallet from numpy.array to dictionary

    Args:
        color_pallet (numpy.array): The color pallet as created by the ColorExtractor.

    Returns:
        dict: The color pallet in dictonary form
    """
    pallet_as_list = color_pallet.tolist()
    return {i+1:tuple(pallet_as_list[i]) for i in range(len(pallet_as_list))}

@app.post("/single-rendered-pallet")
def single_rendered_pallet( amount_colors: int, image_to_process: UploadFile = File(...) ) -> StreamingResponse:
    """Returns an image which showscases the uploaded image next its extracted color pallet.

    Args:
        amount_colors (int): The amount of colors to extract from image_to_process.
        image_to_process (UploadFile): This is the image from which the colors will be extracted.

    Returns:
        StreamingResponse: The rendered image.
    """

    destination_file_path = asyncio.run(save_recived_file(image_to_process))
    loaded_img = load_image_as_array(destination_file_path, resize = SIZE_FOR_LOADED_IMGS)
    color_extractor = ColorExtractor(amount_colors, ITERS_TO_RUN, SIZE_FOR_LOADED_IMGS)
    image = color_extractor.get_rendered_img_pallet(loaded_img)
    memory_stream = io.BytesIO()
    image.save(memory_stream, format="PNG")
    memory_stream.seek(0)
    os.remove(destination_file_path)
    return StreamingResponse(memory_stream, media_type="image/png")

async def save_recived_file(image_to_process) -> str:
    """Saves a recieved file in the server.

    Args:
        image_to_process (UploadFile): Image to save.

    Returns:
        str: The path to the saved file.
    """

    destination_file_path = DIR_IMGS_TO_PROCESS + image_to_process.filename
    async with aiofiles.open(destination_file_path, 'wb') as out_file:
        while content := await image_to_process.read(1024):
            await out_file.write(content)
    return destination_file_path