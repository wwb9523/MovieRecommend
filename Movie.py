import numpy as np
from DB import MyDB

class Movie(object):
    def __init__(self,genres=[0],directories=[0],writers=[0],casts=[0],languages=[0],country=[0],year=0,length=0):
        self.genres=np.array(genres)
        self.directories=np.array(directories)
        self.country=np.array(country)
        self.casts=np.array(casts)
        self.writers=np.array(writers)
        self.languages=np.array(languages)
        self.year=year
        self.length=length

    def getGenres(self):
        return self.genres

    def getDirector(self):
        return self.directories

    def add(self,mov):
        if isinstance(mov,Movie):
            self.casts =self.casts+mov.casts
            self.genres = self.genres +mov.genres
            self.directories = self.directories +mov.directories
            self.country = self.country +mov.country
            self.writers = self.writers +mov.writers
            self.languages = self.languages +mov.languages
            self.year = self.year +mov.year
            self.length = self.length +mov.length

    def sub(self,mov):
        if isinstance(mov, Movie):
            self.casts -= mov.casts
            self.genres -= mov.genres
            self.directories -= mov.directories
            self.country -= mov.country
            self.writers -= mov.writers
            self.languages -= mov.languages
            self.year -= mov.year
            self.length -= mov.length

    def divide(self,n):
        self.casts =self.casts/n
        self.genres = self.genres/n
        self.directories = self.directories/n
        self.country = self.country/n
        self.writers = self.writers/n
        self.languages = self.languages/n
        self.year = self.year/n
        self.length = self.length/n

    def init(self):
        myDB = MyDB()
        self.genresWeight = 2
        self.langWeight = 2
        self.countryWeight = 2
        self.castIndex = {}
        self.directorIndex = {}
        self.writerIndex = {}
        self.castsCount = myDB.getCountCasts()
        self.directorCount = myDB.getCountDirector()
        self.writerCount = myDB.getCountWriter()
        self.casts = np.array([0 for n in range(len(self.castsCount))])
        self.directories = np.array([0 for n in range(len(self.directorCount))])
        self.writers = np.array([0 for n in range(len(self.writerCount))])
        self.languages = np.array([0 for n in range(myDB.getLanguage())])
        self.genres = np.array([0 for n in range(myDB.getGenres())])
        self.country = np.array([0 for n in range(myDB.getCountries())])
        i = 0
        for item in self.castsCount:
            self.castIndex[item[0]] = i
            i = i + 1
        i = 0
        for item in self.directorCount:
            self.directorIndex[item[0]] = i
            i = i + 1
        i = 0
        for item in self.writerCount:
            self.writerIndex[item[0]] = i
            i = i + 1
        myDB.db.close()

    def getMovieById(self,id):
        self.init()
        mydb = MyDB()
        genresRel = mydb.getGenresRela(id)
        countryRel = mydb.getCountryRela(id)
        castsRel = mydb.getCastRela(id)
        directorRel = mydb.getDirectorsRela(id)
        langRel = mydb.getLanguageRela(id)
        writerRel = mydb.getWriterRela(id)
        for item in castsRel:
            self.casts[self.castIndex[item[0]]] = item[1]
        for item in directorRel:
            self.directories[self.directorIndex[item[0]]] = item[1]
        for item in writerRel:
            self.writers[self.writerIndex[item[0]]] = item[1]
        for item in genresRel:
            self.genres[item[0]] = self.genresWeight
        for item in countryRel:
            self.country[item[0]] = self.countryWeight
        for item in langRel:
            self.languages[item[0]] = self.langWeight
        self.year, self.length = mydb.getMovieById(id)
        mydb.db.close()
        return self

    def getList(self):
       # dirc={'genres':self.genres,'director'}
        return self.genres,self.directories,self.writers,self.casts,self.country,self.languages,self.year,self.length