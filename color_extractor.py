from clustering import LloydCluster
from clustering.distance_functions import manhattan_distance as DISTANCE_FUNCTION
from images import load_image_as_array
from images import save_image
import numpy as np

AMOUNT_CLUSTERS    = 5
ITERS_TO_RUN_LLOYD = 5
SIZE_FOR_LOADED_IMGS = (685, 385)
AMOUNT_PIXELS = SIZE_FOR_LOADED_IMGS[0] * SIZE_FOR_LOADED_IMGS[1]
DIR_CREATED_IMGS = "./created_imgs/"
DIR_IMGS_TO_PROCESS = "./base_imgs/"
IMG_NAME = "yes_sr.png"

def main():
    loaded_img     = load_image_as_array(DIR_IMGS_TO_PROCESS + IMG_NAME, resize = SIZE_FOR_LOADED_IMGS)
    color_channels = loaded_img.shape[-1]
    pixel_list     = loaded_img.reshape((AMOUNT_PIXELS, color_channels))
    colorCluster   = LloydCluster(pixel_list, AMOUNT_CLUSTERS, DISTANCE_FUNCTION)
    _ = colorCluster.clustering(ITERS_TO_RUN_LLOYD)
    colors = np.rint(colorCluster.centroids).astype('uint32')
    final_img_name = f"{DIR_CREATED_IMGS}{IMG_NAME.split('.')[0]}-color-pallet.png"
    save_image(loaded_img, colors, final_img_name)

if __name__ == "__main__": main()