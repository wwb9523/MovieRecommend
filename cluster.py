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



    def recommend(self,item=None,k=10,pkl='pkl/clf1000_3_12206952.6048_0.997818572305.pkl'):
        input = open(pkl, 'rb')
        mk = pickle.load(input)
        input.close()
        label = mk._labels
        recom_items = []
        if not item:
            center = mk._centroids
            result={}
            for c in center:
                d1=self.recommend(int(c),5)
                d2=result.copy()
                d2.update(d1)
                result=d2
            return result
        mydb=MyDB()
        item_label=np.nonzero(label==label[item-1])[0]+1
        items=mydb.getMinDistance(item,k)
        mydb.db.close()
        for movId1,movId2,distance in items:
            ritem=lambda x,y: x if y==item else y
            recom_item=ritem(movId1,movId2)
            if recom_item in item_label:
                recom_items.append([recom_item,distance])
        return dict(recom_items)


    def clustering(self,k=3,limit=1000):
        print(k)
        mydb=MyDB()
        movIndex=mydb.getMovieIndex(limit)
        mydb.db.close()
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
    lt=[8,9,6,10,7]
    i=0
    while(True):
        cluster=Cluster()
        cluster.clustering(lt[i],1000)
        i=i+1
        if i>len(lt)-1:
            i=0

