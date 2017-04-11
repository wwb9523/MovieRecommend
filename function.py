import numpy as np
from Movie import Movie

def distMovie(x, y):
    if isinstance(x, Movie) and isinstance(y, Movie):
        listX = x.getList()
        listY = y.getList()
        ds = 0
        for i in range(len(listX)):
            ar1 = np.array(listX[i])
            ar2 = np.array(listY[i])
            d = dist(ar1, ar2)
            ds += d
        return ds


def dist( vect1, vect2):
    return np.sqrt(np.sum(np.square(vect1 - vect2)))