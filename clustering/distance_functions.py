import numpy as np

def manhattan_distance(p1, p2): 
    """Computes the manhattan distances between p1 and p2.

    Args:
        p1 (numpy.array): A 1D numpy array with value of a data point.
        p2 (numpy.array): Can be either another 1D numpy array or a 2D array with a data point in each line.

    Returns:
        numpy.array: An array with the distances between p1 and the points from p2.
    """
    
    return (np.abs(p2 - p1)).sum(axis=1)

def euclidean_distance(p1, p2): 
    """Computes the euclidean distances between p1 and p2.

    Args:
        p1 (numpy.array): A 1D numpy array with value of a data point.
        p2 (numpy.array): Can be either another 1D numpy array or a 2D array with a data point in each line.

    Returns:
        numpy.array: An array with the distances between p1 and the points from p2.
    """

    return np.sqrt(((p2 - p1)**2).sum(axis=1))