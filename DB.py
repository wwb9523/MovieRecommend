#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import sys

class MyDB(object):
    def __init__(self):
        self.db = pymysql.connect(
            host='127.0.0.1',
            port = 3306,
            user='root',
            passwd='',
            db ='test',
            charset='utf8'
            )
        self.cursor=self.db.cursor()

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
            #print('insert distance %s,%s,%s' % (m1, m2,distance))
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
