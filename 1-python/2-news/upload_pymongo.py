from pymongo import MongoClient
import json
import pymongo
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = pymongo.MongoClient("mongodb+srv://detest1:aptx4869@de1.wim4p.mongodb.net/de1?retryWrites=true&w=majority")
db = client.test
db = client.admin
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)

##############
booktable = client.my_database.news_rmrb
data = []
with open('news.json') as f:
    for line in f:
        data.append(json.loads(line))
booktable.insert_many(data)
client.close()
