import sys,os
from Movie import Movie
from DB import MyDB
import numpy as np
from function import distMovie
import pickle

def Silhouette(mk):
    label = mk._labels
    labels={}
    for i in range(mk._k):
        labels.setdefault(i+1,{})
        value = np.nonzero(label == i + 1)[0]
        labels[i+1]=value
    siAll=0
    for i in range(len(mk._labels)):
        si=getSi(labels,i)
        siAll=siAll+si
    Sil=siAll/len(mk._labels)
    print(Sil)
    return Sil


def getAi(labels,i):
    label=[]
    for key,item in labels.items():
        if i in item:
            label=item
            break
    if i not in label:
        return -1
    mydb = MyDB()
    dsAll=0
    for index in label:
        distance = mydb.getSimById(i+1, index+1)
        if not distance:
            movie1 = Movie().getMovieById(i+1)
            movie2 = Movie().getMovieById(index+1)
            distance = distMovie(movie1, movie2)
            mydb.insertDistance(i+1, index+1, distance)
        dsAll=dsAll+distance
    mydb.db.commit()
    mydb.db.close()
    ai=dsAll/len(label)
    return ai


def getBi(labels,i):
    ds=[]
    mydb = MyDB()
    for key, item in labels.items():
        if i in item:
            continue
        dsAll=0
        for index in item:
            distance = mydb.getSimById(i + 1, index + 1)
            if not distance:
                movie1 = Movie().getMovieById(i + 1)
                movie2 = Movie().getMovieById(index + 1)
                distance = distMovie(movie1, movie2)
                mydb.insertDistance(i+1, index+1, distance)
            dsAll = dsAll + distance
        ds.append(dsAll)
    mydb.db.commit()
    mydb.db.close()
    bi=min(ds)
    return bi

def getSi(labels,i):
    ai=getAi(labels,i)
    print('ai: %s'%ai)
    bi=getBi(labels,i)
    print('bi: %s'%bi)
    si=(bi-ai)/max([ai,bi])
    print('si: %s'%si)
    return si

if __name__=='__main__':
    file=sys.argv[1]
    if not os.path.exists(file):
        print('file not exists !')
    if not file.endswith('pkl'):
        print('file must be pkl !')
    input = open(file, 'rb')
    mk = pickle.load(input)
    input.close()
    sil = Silhouette(mk)
    mk._sil = sil
    output = open(file, 'wb')
    pickle.dump(mk, output)
    output.close()
