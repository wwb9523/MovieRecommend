import numpy as np
from Movie import Movie
from DB import MyDB

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


def getAllRel():
    mydb = MyDB()
    mv = {}
    res = mydb.getAllMovie()
    mydb.db.close()
    for row in res:
        movId1 = row[0]
        movId2 = row[1]
        distance = row[2]
        item = mv.get(movId1)
        if item:
            if not item.get(movId2):
                mv[movId1][movId2] = distance
        else:
            mv.setdefault(movId1, {})
            mv[movId1][movId2] = distance
    return mv