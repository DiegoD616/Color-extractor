import numpy as np

class LloydCluster:
    def __init__(self, point_list, k, distance_func, centroids_type = "means"):
        self.k = k
        self.point_list     = point_list
        self.centroid_type  = centroids_type
        self.distance_func  = distance_func
        self.amount_points  = len(point_list)
        self.point_size     = len(point_list[0])
        self.centroids      = point_list[np.random.choice(range(self.amount_points), replace = False, size = k)]
        self.list_distances = np.array([float("inf")]*self.amount_points)
        self.point_to_cluster_idx = np.zeros(self.amount_points)

    def clustering(self, iters):
        for i in range(iters):
            points_cluster_sum = np.zeros((self.k, self.point_size))
            points_per_cluster = np.zeros(self.k)
            for point_idx, point in enumerate(self.point_list):
                idx_nearest_centroid, distance_to_centroid = self.__nearest_centroid(point, self.centroids, self.distance_func)
                self.point_to_cluster_idx[point_idx]      = idx_nearest_centroid
                points_cluster_sum[idx_nearest_centroid] += point
                points_per_cluster[idx_nearest_centroid] += 1
            
            if self.centroid_type == "mediods":
                self.centroids = self.__get_mediods(self.k, self.point_list, self.point_to_cluster_idx, self.distance_func)
            else:
                self.centroids = points_cluster_sum / points_per_cluster.reshape((self.k, 1))

        self.list_distances = self.__get_distances_from_centroid(self.point_list, self.point_to_cluster_idx, self.centroids, self.distance_func)
        return self.get_error(self.list_distances)

    def __nearest_centroid(self, point, centroids, distance_func):
        distances_array = distance_func(point, centroids)
        idx_nearest_centroid = np.argmin(distances_array)
        return (idx_nearest_centroid, distances_array[idx_nearest_centroid])

    def __get_distances_from_centroid(self, point_list, point_to_cluster_idx, centroids, distance_func):
        distances_from_centroid = np.zeros(len(point_list))
        for centroid_idx, centroid in enumerate(centroids):
            points_in_cluster_ids = (point_to_cluster_idx == centroid_idx)
            points_in_cluster     = point_list[points_in_cluster_ids]
            distances = distance_func(centroid, points_in_cluster)
            distances_from_centroid[points_in_cluster_ids] = distances

        return distances_from_centroid

    def get_error(self, list_distances):
        return (list_distances).sum()

    def __get_mediods(self, k, point_list, point_to_cluster_idx, distance_func):
        new_mediods = np.zeros((k, len(point_list[0])))
        for cluster_id in range(k):
            points_in_cluster = point_list[point_to_cluster_idx == cluster_id]
            best_sum_distance = float("inf")
            for point in points_in_cluster:
                sum_distances_to_others = distance_func(point, points_in_cluster).sum()
                if sum_distances_to_others < best_sum_distance: 
                    best_sum_distance       = sum_distances_to_others
                    new_mediods[cluster_id] = point

        return new_mediods