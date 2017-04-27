#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import sys

class MyDB(object):
    def __init__(self):
        self.db = pymysql.connect(
            #host='98.142.140.54',
            host='127.0.0.1',
            port = 3306,
            user='root',
            #passwd='APTX4369',
            passwd='',
            db ='test',
            charset='utf8'
            )
        self.cursor=self.db.cursor()

    def getUser(self,username):
        if not username:
            return None
        sql='select id,user_name,real_name,user_password from user where user_name="%s"'%pymysql.escape_string(username)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if res:
            return res[0]
        return None

    def getPersonById(self,ids):
        if not ids:
            return []
       # ids=tuple(ids)
        sql="select name from person where id in (%s)"
        in_p = ', '.join(map(lambda x: str(x), ids))
        sql=sql % (in_p)
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
        except:
           print(sql)
           return []
        result=[]
        for item in res:
            result.append(item[0])
        return result

    def getLanguageById(self,ids):
        if not ids:
            return []
        sql = "select name from language where id in (%s)"
        in_p = ', '.join(map(lambda x: str(x), ids))
        sql = sql % (in_p)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        result = []
        for item in res:
            result.append(item[0])
        return result

    def getGenresById(self,ids):
        if not ids:
            return []
        sql = "select name from genres where id in (%s)"
        in_p = ', '.join(map(lambda x: str(x), ids))
        sql = sql % (in_p)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        result = []
        for item in res:
            result.append(item[0])
        return result

    def getCountryById(self,ids):
        if not ids:
            return []
        sql = "select name from countries where id in (%s)"
        in_p = ', '.join(map(lambda x: str(x), ids))
        sql = sql % (in_p)
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
        except:
            return None
        result = []
        for item in res:
            result.append(item[0])
        return result

    def getMovInfo(self,id):
        sql='select id,title,aka,year,length,img_url from movie where id=%s'%id
        self.cursor.execute(sql)
        movies = self.cursor.fetchall()
        if  len(movies)>0:
            movie=movies[0]
            info = {'cast': '', 'country': '', 'directory': '', 'genres': '',
                    'language': '', 'writer': '','title':movie[1],'aka':movie[2],'img':movie[5],
                    'length':movie[4],'year':movie[3]
                    }
            id=movie[0]
            print(id)
            castIds=list(map(lambda x:x[0],self.getCastRela(id)))
            countries=list(map(lambda x:x[0],self.getCountryRela(id)))
            direct=list(map(lambda x:x[0],self.getDirectorsRela(id)))
            genres=list(map(lambda x:x[0],self.getGenresRela(id)))
            lang=list(map(lambda x:x[0],self.getLanguageRela(id)))
            writer=list(map(lambda x:x[0],self.getWriterRela(id)))
            info['cast'] = self.getPersonById(castIds)
            info['country']=self.getCountryById(countries)
            info['directory'] = self.getPersonById(direct)
            info['genres'] = self.getGenresById(genres)
            info['language'] = self.getLanguageById(lang)
            info['writer'] = self.getPersonById(writer)
            return info
            # for cast in castIds:

    def getMovieIndex(self,limit=0):
        sql='select id from movie ORDER BY id ASC'
        if limit:
            sql+=' limit %s'%limit
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        list=[]
        for item in res:
            list.append(item[0])
        return list

    #查询所有电影
    def getMovie(self):
        sql='select id from movie order by id ASC'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    # 查询所有电影类别
    def getGenres(self):
        sql='select count(*) from genres'
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        return res[0][0]


    # 查询所有语言
    def getLanguage(self):
        sql='select count(*) from language'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res[0][0]

    #查询所有国家
    def getCountries(self):
        sql = 'select count(*) from countries'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res[0][0]

    #查询导演-电影 关系
    def getDirectorsRela(self,mid):
        sql = 'SELECT personId,dir_weight FROM directors_rela AS a JOIN person AS b WHERE a.movId=%s AND  a.personId=b.id' %(mid)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    #查询类别-电影 关系
    def getGenresRela(self,mid,):
        sql='select genresId from genres_mov where movId=%s'%(mid)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    #查询语言-电影关系
    def getLanguageRela(self,mid):
        sql='select languageId from lang_mov where movId=%s'%(mid)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    #查询编辑-电影 关系
    def getWriterRela(self,mid):
        sql='SELECT personId,writer_weight FROM writers_rela AS a JOIN person AS b WHERE a.movId=%s AND  a.personId=b.id'%(mid)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    #查询国家-电影 关系
    def getCountryRela(self,mid):
        sql='select countryId from country_mov where movId=%s'%(mid)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    #查询主演-电影关系
    def getCastRela(self,mid):
        sql='SELECT personId,cast_weight FROM casts_rela AS a JOIN person AS b WHERE a.movId=%s AND  a.personId=b.id'%(mid)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def getCountCasts(self):
        sql='SELECT personId FROM casts_rela  GROUP BY personId'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def getCountDirector(self):
        sql = 'SELECT personId FROM directors_rela  GROUP BY personId'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def getCountWriter(self):
        sql = 'SELECT personId FROM writers_rela  GROUP BY personId'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def selectDistance(self,movId1,movId2):
        if movId1<movId2:
            m1,m2=movId1,movId2
        else:
            m2,m1=movId1,movId2
        sql='select distance from sim_mov where movId1=%s and movId2=%s'%(m1,m2)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def insertDistance(self,movId1,movId2,distance):
        if movId1<movId2:
            m1,m2=movId1,movId2
        else:
            m2,m1=movId1,movId2
        if not self.selectDistance(m1,m2):
            print('insert distance %s,%s,%s' % (m1, m2,distance))
            sql='insert into sim_mov(movId1,movId2,distance) VALUES(%s,%s,%s)'%(m1,m2,distance)
            return self.cursor.execute(sql)
        else:
            return None

    def getMovieById(self,movId):
        sql='select year,lengths from movie where id=%s'%movId
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res[0][0],res[0][1]

    def getData(self):
        sql='select id,length from movie where statu=0 limit 100'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def updateMovie(self,movId,length):
        sql='update movie set lengths=%s,statu=1 where id=%s'%(length,movId)
        res=self.cursor.execute(sql)
        return res

    def getInitId(self):
        sql='SELECT MAX(movId1),MAX(movId2) FROM sim_mov'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if not res[0][0]:
            res=[[1,1]]
        return res[0][0],res[0][1]

    def getLastId(self):
        sql = 'SELECT MAX(movId2) FROM sim_mov'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if not res[0][0]:
            return 2
        return res[0][0]

    def getMovList(self,id):
        sql='select MAX(movId1) from sim_mov where movId2=%s'%(id)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if not res[0][0]:
            return [[0]]
        return res

    def getCastCount(self,personId):
        sql='SELECT COUNT(*) FROM casts_rela WHERE personId=%s'%personId
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if res:
            return res[0][0]
        else:
            return 0

    def getDirCount(self,personId):
        sql = 'SELECT COUNT(*) FROM directors_rela WHERE personId=%s' % personId
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if res:
            return res[0][0]
        else:
            return 0

    def getWriterCount(self,personId):
        sql = 'SELECT COUNT(*) FROM writers_rela WHERE personId=%s' % personId
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if res:
            return res[0][0]
        else:
            return 0

    def updatePerson(self,personId,cast,dir,writer):
        sql = 'update person set cast_num=%s,cast_weight=%s,' \
              'dir_num=%s,dir_weight=%s,writer_num=%s,writer_weight=%s,' \
              'statu=1 where id=%s' % (cast,cast,dir,dir,writer,writer,personId)
        return self.cursor.execute(sql)

    def getPerson(self):
        sql='select id from person where statu=0 limit 50'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def getSimById(self,id1,id2):
        sql='select distance from sim_mov where (movId2=%s and movId1=%s) or (movId1=%s and movId2=%s)'%(id1,id2,id1,id2)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if res:
            return res[0][0]
        return None

    def insertUData(self,userId,itemId,rating,item):
        sql='insert into udata(user_id,item_id,rating,movieLens_id) values(%s,%s,%s,%s)'%(userId,itemId,rating,item)
        return self.cursor.execute(sql)

    def getAllMovie(self):
        sql='select movId1,movId2,distance from sim_mov'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def getAllScore(self):
        sql='select user_id,item_id,rating from udata'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def insertUser(self,userName,userPassword,email,realName):
        sql='insert into user(user_name,user_password,email,real_name) values("%s","%s","%s","%s")'%(pymysql.escape_string(userName),pymysql.escape_string(userPassword),pymysql.escape_string(email),pymysql.escape_string(realName))
        return  self.cursor.execute(sql)

    def getMinDistance(self,movId1,limit=100):
        #sql='SELECT movId2,distance FROM sim_mov WHERE  distance=(SELECT MIN(distance) FROM sim_mov WHERE (movId1=%s or movId2=%s) AND movId2 != movId1)'%(movId1,movId1)
        sql='SELECT movId1,movId2,distance FROM sim_mov WHERE movId1 != movId2 AND (movId1=%s OR movId2=%s) ORDER BY distance ASC limit %s'%(movId1,movId1,limit)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

