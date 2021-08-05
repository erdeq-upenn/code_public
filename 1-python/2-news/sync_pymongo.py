from bson.json_util import dumps
from pymongo import MongoClient
import json
import pymongo
# pprint library is used to make the output look more pretty
from pprint import pprint

def check_uniqueness(id):
    if newstable.find({'id':id}).count() > 1:
        return False
    return True

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = pymongo.MongoClient("mongodb+srv://detest1:aptx4869@de1.wim4p.mongodb.net/de1?retryWrites=true&w=majority")
db = client.test
db = client.admin
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)

##############
# upload to pymongodb
newstable = client.my_database.news
# data = []
with open('news.json') as f:
    for line in f:
        if check_uniqueness(json.loads(line)['id']):
            newstable.insert_one(json.loads(line))
f.close()
        # print(json.loads(line)['id'])
#         data.append(json.loads(line))
# newstable.insert_many(data)

# sync db
cursor = newstable.find({})
with open('news_db.json', 'w') as file:
    for document in cursor:
        file.write(dumps(document,ensure_ascii=False))
        file.write(',\n')
file.close()
client.close()
