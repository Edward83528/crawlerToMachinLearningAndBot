# -*- coding: utf-8 -*-
import pymongo as mg
import datetime

client = mg.MongoClient('127.0.0.1:27017')
db = client['uuutest'] #DBName: uuutest

#post is collection name
result = db.post.insert_one(
{
    "title": 'Headline of the day',
    "body":'blah blah blah...',
    "datetime":datetime.datetime.now()
} )

result = db['post'].find({})
lst  =  list(result)

for x in lst:
    print(x['title'])
    print(x['body'])
    print(str(x['datetime']))