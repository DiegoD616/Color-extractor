from PIL import Image, ImageDraw, ImageFont
from itertools import product
import numpy as np

DIR_CREATED_IMGS = "./created_imgs/"
SIZE_FOR_LOADED_IMGS = (685, 385)
AMOUNT_PIXELS = SIZE_FOR_LOADED_IMGS[0] * SIZE_FOR_LOADED_IMGS[1]
AMOUNT_EXPERIMENT_REPETIONS = 3
AMOUNT_CLUSTERS    = 5
ITERS_TO_RUN_LLOYD = 5
CLUSTER_TYPES      = ["means", "mediods"]
DISTANCE_FUNCTIONS = ["euclidean", "manhattan"]
FILES_TO_PROCESS   = [
    "el_el_le_elegance.png", 
    "i_feel_like_i_can_do_it.png", 
    "se_murieron_xd.png",
    "xd_2.png", 
    "yes_sr.png",
]

def main():
    experiment_combinations = product(
        FILES_TO_PROCESS, product(CLUSTER_TYPES, DISTANCE_FUNCTIONS)
    )

    for img_name, (cluster_type, distance_function) in experiment_combinations:
        best_results = (None, float("inf"))
        for experiment in range(AMOUNT_EXPERIMENT_REPETIONS):
            loaded_img = load_image(
                "base_imgs/" + img_name, resize = SIZE_FOR_LOADED_IMGS
            ).astype("float32")
            color_channels = loaded_img.shape[-1]
            
            colors, error = lloyd(
                loaded_img.reshape((AMOUNT_PIXELS, color_channels)), 
                AMOUNT_CLUSTERS, ITERS_TO_RUN_LLOYD,
                cluster_type, distance_function
            )
            if error < best_results[1]: best_results = (np.rint(colors).astype(np.uint8), error)
        
        plot_image(
            loaded_img, best_results[0], (cluster_type, distance_function), error,
            show=False, save=True, 
            name=f"{img_name}-best-color-pallet_{cluster_type}_{distance_function}.png"
        )

def load_image(filename, resize=None, color_mode = "RGB"):
    img = Image.open(filename).convert(color_mode)
    if resize is not None: img = img.resize(resize)
    return np.array(img)

def lloyd(point_list, k, iters, centroids_type, distance):
    amount_points = len(point_list)
    point_size    = len(point_list[0])
    point_to_cluster_idx = np.zeros(amount_points)
    distance_func = get_distance_function(distance)
    centroids = point_list[np.random.choice(range(amount_points), replace = False, size = k)]

    for i in range(iters):
        points_cluster_sum = np.zeros((k, point_size))
        points_per_cluster = np.zeros(k)
        for point_idx, point in enumerate(point_list):
            idx_nearest_centroid, distance_to_centroid = nearest_centroid(point, centroids, distance_func)
            point_to_cluster_idx[point_idx] = idx_nearest_centroid
            points_cluster_sum[idx_nearest_centroid] += point
            points_per_cluster[idx_nearest_centroid] += 1
        
        list_distances = get_distances_from_centroid(point_list, point_to_cluster_idx, centroids, distance_func)
        error = get_error(list_distances)
        
        if centroids_type == "mediods":
            centroids = get_mediods(k, point_list, point_to_cluster_idx, distance_func)
        else:
            centroids = points_cluster_sum / points_per_cluster.reshape((k, 1))

    return (centroids, error)

def get_distance_function(distance):
    if   distance == "euclidean": return euclidean_distance
    elif distance == "manhattan": return manhattan_distance
    else: raise ValueError("Distance function not found")

def nearest_centroid(point, centroids, distance_func):
    distances_array = distance_func(point, centroids)
    idx_nearest_centroid = np.argmin(distances_array)
    return (idx_nearest_centroid, distances_array[idx_nearest_centroid])

def manhattan_distance(p1, p2): return (np.abs(p2 - p1)).sum(axis=1)
def euclidean_distance(p1, p2): return np.sqrt(((p2 - p1)**2).sum(axis=1))

def get_distances_from_centroid(point_list, point_to_cluster_idx, centroids, distance_func):
    distances_from_centroid = np.zeros(len(point_list))
    for centroid_idx, centroid in enumerate(centroids):
        points_in_cluster_ids = (point_to_cluster_idx == centroid_idx)
        points_in_cluster     = point_list[points_in_cluster_ids]
        distances = distance_func(centroid, points_in_cluster)
        distances_from_centroid[points_in_cluster_ids] = distances

    return distances_from_centroid

def get_error(list_distances):
    return (list_distances).sum()

def get_mediods(k, point_list, point_to_cluster_idx, distance_func):
    new_mediods = np.zeros((k, len(point_list[0])))
    for cluster_id in range(k):
        points_in_cluster = point_list[point_to_cluster_idx == cluster_id]
        best_sum_distance = float("inf")
        for point in points_in_cluster:
            sum_distances_to_others = distance_func(point, points_in_cluster).sum()
            if sum_distances_to_others < best_sum_distance: 
                best_sum_distance = sum_distances_to_others
                new_mediods[cluster_id] = point

    return new_mediods

def plot_image(img, color_pallet, experiment_comb, error, show=True,save=False,name=None):
    result = get_canvas_result(img)
    draw = ImageDraw.Draw(result)
    draw.text((10, 10), "Paleta de colores\n" + str(experiment_comb), size=250, fill="black")
    add_color_pallet(draw, color_pallet)
    draw.text((10, 365), "Error: {:.2e}".format(error), size=150, fill="black")

    if show: result.show()
    if save: result.save(DIR_CREATED_IMGS+name)

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
            size=300, fill="black"
        )
        
        color_square_size_begin += color_square_size
        color_square_size_end   = color_square_size_begin + color_square_size

def rgb_to_hex(rgb): return "#{:02X}{:02X}{:02X}".format(*rgb)

if __name__ == "__main__": main()