import numpy as np

class Movie(object):
    def __init__(self,genres,directories):
        self.genres=genres
        self.directories=directories

    def getGenres(self):
        return self.genres

    def getList(self):
        return self.genres,self.directories,[]