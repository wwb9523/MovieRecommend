#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,random
from DB import MyDB
from faker import Faker
fake = Faker()

def dealUdata():
    mydb = MyDB()
    train_file = 'ml-100k/u.data'
    item_movie = {}
    i = 1
    for line in open(train_file):
        user, item, score, _ = line.strip().split("\t")
        if item in item_movie.keys():
            item_id = item_movie[item]
        else:
            item_movie.setdefault(item, 0)
            item_movie[item] = i
            item_id = i
            i = i + 1
        mydb.insertUData(int(user), int(item_id), float(score), int(item))
    mydb.db.commit()
    mydb.db.close()

def dealUserInfo():
    mydb = MyDB()
    for _ in range(100):
        user = fake.simple_profile()
        mydb.insertUser(user['username'],user['birthdate'].replace('-',''),user['mail'],user['name'])
    mydb.db.commit()
    mydb.db.close()

if __name__=='__main__':
    dealUserInfo()

