import sys,os
from Movie import Movie
from DB import MyDB
import numpy as np
from function import distMovie,getAllRel
import pickle,time

sim=getAllRel()

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
    global sim
    for key,item in labels.items():
        if i in item:
            label=item
            break
    if i not in label:
        return -1
    dsAll=0
    for index in label:
        distance = sim.get(min(i+1,index+1)).get(max(i+1, index+1))
        if not distance:
            mydb = MyDB()
            movie1 = Movie().getMovieById(i+1)
            movie2 = Movie().getMovieById(index+1)
            distance = distMovie(movie1, movie2)
            mydb.insertDistance(i+1, index+1, distance)
            mydb.db.commit()
            mydb.db.close()
        dsAll=dsAll+distance
    ai=dsAll/len(label)
    return ai


def getBi(labels,i):
    ds=[]
    global sim
    for key, item in labels.items():
        if i in item:
            continue
        dsAll=0
        for index in item:
            movId1=min(i + 1, index+1)
            movId2=max(i + 1, index + 1)
            distance = sim.get(movId1).get(movId2)
            if not distance:
                mydb = MyDB()
                movie1 = Movie().getMovieById(movId1)
                movie2 = Movie().getMovieById(movId2)
                distance = distMovie(movie1, movie2)
                mydb.insertDistance(movId1, movId2, distance)
                sim.setdefault(movId1, {})
                sim[movId1][movId2] = distance
                mydb.db.commit()
                mydb.db.close()
            dsAll = dsAll + distance
        ds.append(dsAll)
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

def silPkl(file):
    if not os.path.exists(file):
        print('file not exists !')
    if not file.endswith('pkl'):
        print('file must be pkl !')
    input = open(file, 'rb')
    mk = pickle.load(input)
    input.close()
    if hasattr(mk,'_sil') and mk._sil:
        print('sil is exists!')
        return -1
    else:
        sil = Silhouette(mk)
        mk._sil = sil
        index=file.rfind('.')
        new_file=file[:index]+'_'+str(sil)+file[index:]
        output = open(new_file, 'wb')
        pickle.dump(mk, output)
        output.close()

if __name__=='__main__':
    time1=time.time()
    file='pkl/clf1000_5_12434580.0478.pkl'
    silPkl(file)
    time2=time.time()
    print('total time: '+str(time2-time1))

