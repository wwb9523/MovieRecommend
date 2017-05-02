import numpy as np
from Movie import Movie
from DB import MyDB
import multiprocessing
from kmeans import KMeansClassifier
import pickle
import os,time


class Cluster(object):
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


    def recommend(self,item,k,pkl='pkl/clf1000_4_11309989.1559.pkl'):
        mydb=MyDB()
        input = open(pkl, 'rb')
        mk = pickle.load(input)
        input.close()
        label = mk._labels
        item_label=np.nonzero(label==label[item-1])[0]+1
        items=mydb.getMinDistance(item,k)
        recom_items=[]
        for movId1,movId2,distance in items:
            ritem=lambda x,y: x if y==item else y
            recom_item=ritem(movId1,movId2)
            if recom_item in item_label:
                recom_items.append(recom_item)
        return recom_items


    def clustering(self,k=3,limit=1000):
        print(k)
        mydb=MyDB()
        movIndex=mydb.getMovieIndex(limit)
        clf = KMeansClassifier(k)
        clf.fit_sim(movIndex)
       # print(clf._labels)
      #  print(clf._centroids)
        pkl="pkl/clf"+str(limit)+"_"+str(k)+'_'+str(clf._sse)+".pkl"
        if os.path.exists(pkl):
            input=open(pkl,'rb')
            mk=pickle.load(input)
            input.close()
            if mk._sse<clf._sse:
                print("return")
                return
        print('pickle!')
        output = open(pkl, 'wb')
        pickle.dump(clf,output)
        output.close()

def run(k=3):
    print(k)
    cluster = Cluster()
    cluster.clustering(k)

def loop():
    list_k=[4,5,6,7,8]
    p = multiprocessing.Pool()
    for k in list_k:
        p.apply_async(run(k),args=(k))
    p.close()
    p.join()

if __name__=='__main__':
    # cluster = Cluster()
    # cluster.recommend(5,3)
    #loop()
    while(True):
        t1=time.time()
        cluster=Cluster()
        cluster.clustering(3,1000)
        t2=time.time()
        print(t2-t1)

