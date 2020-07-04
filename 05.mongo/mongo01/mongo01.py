# -*- coding: utf-8 -*-
import pymongo as mg

client = mg.MongoClient('127.0.0.1:27017') # mongo預設port 27017
db = client['local']
result = db['startup_log'].find({})
lst  =  list(result)

for x in lst:
    print(x['startTime'])
