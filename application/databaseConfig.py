from flask_pymongo import PyMongo
from logger import log

try:
    mongo = PyMongo()
    log.debug("connection to mongoDB database is successful")

except:
    log.error("Error in connecting to mongoDB Database")