from flask import Flask
from flask import request
#from flask_pymongo import PyMongo
import pymongo
from bson.json_util import dumps
import json
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)
## Create a MongoDB client, open a connection to Amazon DocumentDB as a replica set and specify the read preference as secondary preferred
mongo = pymongo.MongoClient('mongodb://group1220:group1220@docdb-2020-04-05-23-50-44.cluster-c1fknw6gmcpf.us-east-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false')

db = mongo.tourist

##Specify the collection to be used
col = db.my_collection

@app.route('/<keyword>', methods=['GET'])
def getPlace(keyword):
    st = '.*' + keyword + '.*'
    regx = re.compile(st, re.IGNORECASE)
    #regx = re.compile('.*keyword.*', re.IGNORECASE)
    places = col.find({"$or": [{"province": regx}, {"city": regx}, {"place": regx}]})
    return dumps(places, indent = 4)

@app.route('/getById/<id>', methods=['GET'])
def getPlaceById(id):

    place = col.find({"id" : int(id)})
    return dumps(place, indent = 4)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True)
