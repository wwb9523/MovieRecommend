import numpy as np
from Movie import Movie
from DB import MyDB
import multiprocessing
from kmeans import KMeansClassifier
import pickle
import os,time


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
        pkl="clf"+str(limit)+"_"+str(k)+'_'+str(clf._sse)+".pkl"
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



if __name__=='__main__':
    loop()
    # while(True):
    #     t1=time.time()
    #     recommend=Recommend()
    #     recommend.clustering()
    #     t2=time.time()
    #     print(t2-t1)

