from clustering import LloydCluster
from clustering.distance_functions import manhattan_distance as DISTANCE_FUNCTION
from images import rendered_img
import numpy as np

class ColorExtractor:
    def __init__(self, amount_colors, iters_to_run, img_sizes):
        self.amount_clusters = amount_colors
        self.iters_to_run_clustering = iters_to_run
        self.amount_pixels = img_sizes[0] * img_sizes[1]

    def get_rendered_img_pallet(self, loaded_img):
        color_pallet   = self.get_color_pallet(loaded_img)
        image = rendered_img(loaded_img, color_pallet)
        return image

    def get_color_pallet(self, loaded_img):
        color_channels = loaded_img.shape[-1]
        pixel_list     = loaded_img.reshape((self.amount_pixels, color_channels))
        colorCluster   = LloydCluster(pixel_list, self.amount_clusters, DISTANCE_FUNCTION)
        _ = colorCluster.clustering(self.iters_to_run_clustering)
        colors = np.rint(colorCluster.centroids).astype('uint32')
        return colors