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
def single_pallet( amount_colors: int, image_to_process: UploadFile = File(...) ):
    destination_file_path = asyncio.run(save_recived_file(image_to_process))
    loaded_img = load_image_as_array(destination_file_path, resize = SIZE_FOR_LOADED_IMGS)
    color_extractor = ColorExtractor(amount_colors, ITERS_TO_RUN, SIZE_FOR_LOADED_IMGS)
    color_pallet = color_extractor.get_color_pallet(loaded_img).tolist()
    os.remove(destination_file_path)
    return {i+1:tuple(color_pallet[i]) for i in range(len(color_pallet))}

@app.post("/single-rendered-pallet")
def single_rendered_pallet( amount_colors: int, image_to_process: UploadFile = File(...) ):
    destination_file_path = asyncio.run(save_recived_file(image_to_process))
    loaded_img = load_image_as_array(destination_file_path, resize = SIZE_FOR_LOADED_IMGS)
    color_extractor = ColorExtractor(amount_colors, ITERS_TO_RUN, SIZE_FOR_LOADED_IMGS)
    image = color_extractor.get_rendered_img_pallet(loaded_img)
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