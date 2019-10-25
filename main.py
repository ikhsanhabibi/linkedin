import requests

import indeed, linkedin, simplyhired

bots = ['indeed','linkedin', 'simplyhired']

modules = map(__import__, bots)

import multiprocessing

multiprocessing.Process(target=modules)




import csv
import json

fieldnames = ("Title","Company","City","Country","Internship","Fulltime","Parttime","Summary","Email","Website","Source","PostedDate","ScrapeDate")
with open('jobs.csv', 'r', encoding='utf8') as csvfile:
    with open('jobs.json', 'w', encoding='utf8') as jsonfile:
        reader = csv.DictReader(csvfile, fieldnames, delimiter=',')
        json.dump(list(reader), jsonfile)




from pymongo import MongoClient
import json

HOST,PORT = ('localhost',27017)
DATABASE_NAME = 'ng8crud'
COLLECTION_NAME = 'Job'

client = MongoClient(HOST,PORT) #Connect to Mongo db

db = client[DATABASE_NAME] #Connect to specific database
collection = db[COLLECTION_NAME] #Access specific collection

#db.drop_collection('jobs')

#Then you would need to load a json into a dict(post) then post it using
with open('jobs.json', 'r', encoding='utf-8') as sample:
    for line in sample:
        line = json.loads(line.strip())
        collection.insert_many(line)

client.close()