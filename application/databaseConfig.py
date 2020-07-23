from flask import Flask
from flask_pymongo import pymongo

from logger import log
CONNECTION_STRING = "mongodb+srv://tracksentiments2020:track2020@cluster0.yse0l.mongodb.net/tracksentiments?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

try:
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.get_database('tracksentiments')

    log.debug("connection to mongoDB database is successful")

except:
    log.error("Error in connecting to mongoDB Database")