import numpy as np

def manhattan_distance(p1, p2): return (np.abs(p2 - p1)).sum(axis=1)
def euclidean_distance(p1, p2): return np.sqrt(((p2 - p1)**2).sum(axis=1))