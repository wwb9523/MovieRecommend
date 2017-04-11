import numpy as np
from Movie import Movie
from DB import MyDB
from kmeans import KMeansClassifier
import pickle
import os,time

class Recommend(object):
    def __init__(self,k=3, initCent='random', max_iter=500):
        # myDB = MyDB()
        # self.genresWeight=2
        # self.langWeight=2
        # self.countryWeight=2
        # self.castIndex = {}
        # self.directorIndex = {}
        # self.writerIndex = {}
        # self.castsCount = myDB.getCountCasts()
        # self.directorCount = myDB.getCountDirector()
        # self.writerCount = myDB.getCountWriter()
        # self.castsEmpty = [0 for n in range(len(self.castsCount))]
        # self.directorEmpty = [0 for n in range(len(self.directorCount))]
        # self.writerEmpty = [0 for n in range(len(self.writerCount))]
        # self.langEmpty = [0 for n in range(myDB.getLanguage())]
        # self.genresEmpty = [0 for n in range(myDB.getGenres())]
        # self.countryEmpty = [0 for n in range(myDB.getCountries())]
        # i = 0
        # for item in self.castsCount:
        #     self.castIndex[item[0]] = i
        #     i = i + 1
        # i = 0
        # for item in self.directorCount:
        #     self.directorIndex[item[0]] = i
        #     i = i + 1
        # i = 0
        # for item in self.writerCount:
        #     self.writerIndex[item[0]] = i
        #     i = i + 1
        # myDB.db.close()
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

    # def getMovie(self,id):
    #     mydb=MyDB()
    #     casts=self.castsEmpty
    #     director=self.directorEmpty
    #     writer=self.writerEmpty
    #     lang=self.langEmpty
    #     genres=self.genresEmpty
    #     country=self.countryEmpty
    #     genresRel = mydb.getGenresRela(id)
    #     countryRel = mydb.getCountryRela(id)
    #     castsRel = mydb.getCastRela(id)
    #     directorRel = mydb.getDirectorsRela(id)
    #     langRel = mydb.getLanguageRela(id)
    #     writerRel = mydb .getWriterRela(id)
    #     for item in castsRel:
    #         casts[self.castIndex[item[0]]]=item[1]
    #     for item in directorRel:
    #         director[self.directorIndex[item[0]]]=item[1]
    #     for item in writerRel:
    #         writer[self.writerIndex[item[0]]]=item[1]
    #     for item in genresRel:
    #         genres[item[0]]=self.genresWeight
    #     for item in countryRel:
    #         country[item[0]]=self.countryWeight
    #     for item in langRel:
    #         lang[item[0]]=self.langWeight
    #     year,length=mydb.getMovieById(id)
    #     movie=Movie(genres,director,casts,lang,country,year,length)
    #     mydb.db.close()
    #     return movie


    def clustering(self):
        mydb=MyDB()
        limit=1000
        movIndex=mydb.getMovieIndex(limit)
        k = 3
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

if __name__=='__main__':
    input = open("clf1000_3.pkl", 'rb')
    mk = pickle.load(input)
    input.close()
    print(mk._sse)
    # while(True):
    #     t1=time.time()
    #     recommend=Recommend()
    #     recommend.clustering()
    #     t2=time.time()
    #     print(t2-t1)

