from clustering import LloydCluster
from clustering.distance_functions import manhattan_distance as DISTANCE_FUNCTION
from images import load_image_as_array, rendered_img
from PIL    import Image

import numpy as np
import os

import aiofiles
import asyncio
import io
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, StreamingResponse

AMOUNT_CLUSTERS      = 5
ITERS_TO_RUN_LLOYD   = 5
SIZE_FOR_LOADED_IMGS = (685, 385)
AMOUNT_PIXELS = SIZE_FOR_LOADED_IMGS[0] * SIZE_FOR_LOADED_IMGS[1]
DIR_IMGS_TO_PROCESS = "./base_imgs/"

app = FastAPI()

@app.post("/single-pallet")
def single_pallet( image_to_process: UploadFile = File(...) ):
    destination_file_path = asyncio.run(save_recived_file(image_to_process))
    loaded_img = load_image_as_array(destination_file_path, resize = SIZE_FOR_LOADED_IMGS)
    color_pallet = get_color_pallet(loaded_img).tolist()
    os.remove(destination_file_path)
    return {i+1:tuple(color_pallet[i]) for i in range(len(color_pallet))}

@app.post("/single-rendered-pallet")
def single_rendered_pallet( image_to_process: UploadFile = File(...) ):
    destination_file_path = asyncio.run(save_recived_file(image_to_process))
    image = get_rendered_img_pallet(destination_file_path)
    memory_stream = io.BytesIO()
    image.save(memory_stream, format="PNG")
    memory_stream.seek(0)
    os.remove(destination_file_path)
    return StreamingResponse(memory_stream, media_type="image/png")

async def save_recived_file(image_to_process):
    destination_file_path = DIR_IMGS_TO_PROCESS + image_to_process.filename
    async with aiofiles.open(destination_file_path, 'wb') as out_file:
        while content := await image_to_process.read(1024):
            await out_file.write(content)
    return destination_file_path

def get_rendered_img_pallet(img_name):
    loaded_img     = load_image_as_array(img_name, resize = SIZE_FOR_LOADED_IMGS)
    color_pallet   = get_color_pallet(loaded_img)
    image = rendered_img(loaded_img, color_pallet)
    return image

def get_color_pallet(loaded_img):
    color_channels = loaded_img.shape[-1]
    pixel_list     = loaded_img.reshape((AMOUNT_PIXELS, color_channels))
    colorCluster   = LloydCluster(pixel_list, AMOUNT_CLUSTERS, DISTANCE_FUNCTION)
    _ = colorCluster.clustering(ITERS_TO_RUN_LLOYD)
    colors = np.rint(colorCluster.centroids).astype('uint32')
    return colors