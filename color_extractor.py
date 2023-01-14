from clustering import LloydCluster
from clustering.distance_functions import manhattan_distance as DISTANCE_FUNCTION
from images import rendered_img
import numpy as np

class ColorExtractor:
    """
    A class used to create color pallets from images.

    ...
    Attributes
    ----------
    amount_clusters: int
        The amount of colors to be extracted from the images.
    
    iters_to_run_clustering: int 
        Iterations to run the clustering algorithm.

    amount_pixels: int
        The amount of pixels each image contains.

    Methods
    -------
    get_rendered_img_pallet(loaded_img)
        Returns an image with the loaded_img's color pallet.

    get_color_pallet(loaded_img)
        Returns the a numpy.array with the loaded_img's collor pallet.    
    """

    def __init__(self, amount_colors: int, iters_to_run: int, img_sizes: tuple):
        """
        Args:
            amount_colors (int): The amount of colors to extract from the images.
            iters_to_run (int): Iterations to run the clustering algorithm.
            img_sizes (tuple): The image's dimentions.
        """

        self.amount_clusters = amount_colors
        self.iters_to_run_clustering = iters_to_run
        self.amount_pixels = img_sizes[0] * img_sizes[1]

    def get_rendered_img_pallet(self, loaded_img):
        """Returns an image with the loaded_img's color pallet.

        Args:
            loaded_img (Pillow.Image): An image to get the color pallet from.

        Returns:
            Pillow.Image: The loaded image next to the extracted color pallet.
        """

        color_pallet   = self.get_color_pallet(loaded_img)
        image = rendered_img(loaded_img, color_pallet)
        return image

    def get_color_pallet(self, loaded_img):
        """_summary_

        Args:
            loaded_img (Pillow.Image): An image to get the color pallet from.

        Returns:
            Numpy.array: The color pallet extracted from the image.
        """

        color_channels = loaded_img.shape[-1]
        pixel_list     = loaded_img.reshape((self.amount_pixels, color_channels))
        colorCluster   = LloydCluster(pixel_list, self.amount_clusters, DISTANCE_FUNCTION)
        _ = colorCluster.clustering(self.iters_to_run_clustering)
        colors = np.rint(colorCluster.centroids).astype('uint32')
        return colors