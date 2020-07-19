from flask import Flask
from flask_cors import CORS
import os
from application.databaseConfig import mongo
import application.config as cfg

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY = b';y\xd3\xd3\xe5\xa6\x119(&;Ea\x17\xfe\xdc',
        REDIS_URL = cfg.REDIS_URL,
        MONGO_URI = cfg.MONGO_DB_URI
    )
 

    mongo.init_app(app)

    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from apirouter.getproductdetails import getproducts
    app.register_blueprint(getproducts)

    from apirouter.getreviews import getreviews
    app.register_blueprint(getreviews)

    return app