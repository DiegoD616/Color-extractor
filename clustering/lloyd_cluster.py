import numpy as np

class LloydCluster:
    """
    A class used to cluster data using the Lloyd clustering algorithm.

    ...
    Attributes
    ----------
    k: int
		Amount of clusters.
    point_list: numpy.array
		Data points to be clustered.
    centroid_type: str
		The type of centroid to be used. Can be means or mediods.
    distance_func: function
		The distance function to calculate the distances during clustering.
    amount_points: int
		The amount of point to be clustered.
    point_size: 
		The dimentions of for the data points.
    centroids: 
		The center points for every cluster.
    list_distances: 
		The distances between each point and it's centroid.
    point_to_cluster_idx: 
		An array where the index is the data point and the data at the index is the cluster the point belongs to.

    Methods
    -------
    clustering(iters):
        Runs the clustering algorithm iters iterations.

    get_error(list_distances):
        Returns the error, which is the sum of distances between each point and its centroid.
    """

    def __init__(self, point_list, k, distance_func, centroids_type = "means"):
        """
        Args:
            point_list (numpy.array): Data points to be clustered.
            k (int): Amount of clusters.
            distance_func (function): The distance function to calculate the distances during clustering.
            centroids_type (str, optional): The type of centroid to be used. Can be means or mediods. Defaults to "means".
        """

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
        """Runs the clustering algorithm

        Args:
            iters (int): Amount of interations.

        Returns:
            int: The error after the last iteration.
        """

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
        """Returns the centroid closer to a given point.

        Args:
            point (numpy.array): The point use as a center.
            centroids (numpy.array): The list of posible closer centroids.
            distance_func (function): The functions to be get distances.

        Returns:
            numpy.array: The closer centroid to the given point.
        """

        distances_array = distance_func(point, centroids)
        idx_nearest_centroid = np.argmin(distances_array)
        return (idx_nearest_centroid, distances_array[idx_nearest_centroid])

    def __get_distances_from_centroid(self, point_list, point_to_cluster_idx, centroids, distance_func):
        """Returns the distances of each point to its centroid.

        Args:
            point_list (numpy.array): An array with the data points. A 2D numpy.array.
            point_to_cluster_idx (numpy.array): An index which tell us to what cluster each point belongs to.
            centroids (numpy.array): An array with centroids of each cluster.
            distance_func (function): A function to calculate distances. 

        Returns:
            numpy.array: An array with the distane between each point and its centroid.
        """
        
        distances_from_centroid = np.zeros(len(point_list))
        for centroid_idx, centroid in enumerate(centroids):
            points_in_cluster_ids = (point_to_cluster_idx == centroid_idx)
            points_in_cluster     = point_list[points_in_cluster_ids]
            distances = distance_func(centroid, points_in_cluster)
            distances_from_centroid[points_in_cluster_ids] = distances

        return distances_from_centroid

    def get_error(self, list_distances):
        """Returns the clustering error.

        Args:
            list_distances (numpy.array): An array with the distences beetween each point and its centroid.

        Returns:
            int: The sum of the distances.
        """

        return (list_distances).sum()

    def __get_mediods(self, k, point_list, point_to_cluster_idx, distance_func):
        """Return an array with the new centroids, calculated as mediods.

        Args:
            k (int): The amount of clusters.
            point_list (numpy.array): An array of data points.
            point_to_cluster_idx (numpy.array): An index which tell us to what cluster each point belongs to.
            distance_func (function): A function to calculate distances.

        Returns:
            numpy.array: An array with the new centroids.
        """


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