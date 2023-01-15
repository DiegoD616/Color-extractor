"""API - Main

This script allows the user to start a uvicorn server which runs the api's app

"""
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, StreamingResponse, RedirectResponse

from color_extractor import ColorExtractor
from images import load_image_as_array

ITERS_TO_RUN = 1
SIZE_FOR_LOADED_IMGS = (685, 385)

app = FastAPI()

@app.get("/")
def root():
    """The root dir redirects to the docs because right now there's nothing at the root."""

    response = RedirectResponse(url='/docs')
    return response


@app.post("/single-pallet")
async def single_pallet( amount_colors: int, image_to_process: UploadFile = File(...) ) -> dict:
    """Returns a dictionary with the image's most relevant colors as the values and integers as the keys.
    The color will be returned in RGB format.

    Args:
        amount_colors (int): The amount of colors to extract from image_to_process
        image_to_process (UploadFile): This is the image from which the colors will be extracted.

    Returns:
        dict: A dictionary with the most relevant colors
    """

    loaded_img = load_image_as_array(image_to_process.file, resize = SIZE_FOR_LOADED_IMGS)
    color_extractor = ColorExtractor(amount_colors, ITERS_TO_RUN, SIZE_FOR_LOADED_IMGS)
    color_pallet = color_extractor.get_color_pallet(loaded_img)
    return color_pallet_to_dic(color_pallet)

def color_pallet_to_dic(color_pallet) -> dict:
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

    loaded_img = load_image_as_array(image_to_process.file, resize = SIZE_FOR_LOADED_IMGS)
    color_extractor = ColorExtractor(amount_colors, ITERS_TO_RUN, SIZE_FOR_LOADED_IMGS)
    image_stream = color_extractor.get_rendered_img_pallet(loaded_img, True)
    return StreamingResponse(image_stream, media_type="image/png")