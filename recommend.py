import numpy as np
from Movie import Movie
from DB import MyDB
import multiprocessing
from kmeans import KMeansClassifier
import pickle
import os,time
from function import distMovie

class Recommend(object):
    def __init__(self,k=3, initCent='random', max_iter=500):
        self._k = k
        self._initCent = initCent
        self._max_iter = max_iter
        self._clusterAssment = None
        self._labels = None
        self._sse = None


    def distMovie(self,x,y):
        if isinstance(x,Movie) and isinstance(y,Movie):
            listX=x.getList()
            listY=y.getList()
            ds=0
            for i in listX:
                d=self.dist(listX[i],listY[i])
                ds+=d
            return ds

    def dist(self,vect1,vect2):
        return np.sqrt(np.sum(np.square(vect1 - vect2)))

    def clustering(self,k=3):
        print(k)
        mydb=MyDB()
        limit=1000
        movIndex=mydb.getMovieIndex(limit)
        clf = KMeansClassifier(k)
        clf.fit_sim(movIndex)
        print(clf._labels)
        print(clf._centroids)
        print(clf._sse)
        pkl="clf"+str(limit)+"_"+str(k)+".pkl"
        if os.path.exists(pkl):
            input=open(pkl,'rb')
            mk=pickle.load(input)
            input.close()
            print(mk._sse)
            if mk._sse<clf._sse:
                print("return")
                return
        print('pickle!')
        output = open(pkl, 'wb')
        pickle.dump(clf,output)
        output.close()

def run(k=3):
    print(k)
    recommend = Recommend()
    while True:
        recommend.clustering(k)

def loop():
    list_k=[4,5,6,7,8]
    run_list=[]
    p = multiprocessing.Pool()
    for k in list_k:
        p.apply_async(run(k),args=(k))
    p.close()
    p.join()

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
    #loop()
    pkl="clf1000_3.pkl"
    input = open(pkl, 'rb')
    mk = pickle.load(input)
    input.close()
    sil=Silhouette(mk)
    mk._sil=sil
    output = open(pkl, 'wb')
    pickle.dump(mk, output)
    output.close()
    # while(True):
    #     t1=time.time()
    #     recommend=Recommend()
    #     recommend.clustering()
    #     t2=time.time()
    #     print(t2-t1)

