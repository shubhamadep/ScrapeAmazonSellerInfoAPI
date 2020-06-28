from flask_mongoalchemy import MongoAlchemy
from app import app
from logger import log
import config as cfg

app.config['MONGOALCHEMY_DATABASE'] = cfg.MONGO_DB_DATABASE
app.config['MONGOALCHEMY_CONNECTION_STRING'] = cfg.MONGO_DB_URL

db = "DBConnection"
try:
    db = MongoAlchemy(app)
    log.debug("connection to mongoDB database is successfull")

except:
    log.error("Error in connecting to mongoDB database")