"""
    This package provides a class for clustering and a sub-package with functions to calculate the distances
    between vetors.

    Classes
    -------
    LloydCluster
        A class which does clustering with a list of data points.

    Sub-packages
    ------------
    distance_functions
        Provides functions to calculate distances between vectors.
"""

from .lloyd_cluster import LloydCluster
from . import distance_functions