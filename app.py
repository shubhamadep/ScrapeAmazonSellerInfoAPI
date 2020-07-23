import crochet
crochet.setup()
import flask
from application import create_app
from flask_redis import FlaskRedis
from application import databaseConfig
from flask_pymongo import pymongo
#MongoDB imports

app = create_app()
redis_client = FlaskRedis(app)

"""MongoDB Server Instance Testing"""

@app.route("/mongoDBTest/all", methods=["GET"])
def getAllProductInfo():
    testProduct = productInfo.productInfo.query.all()
    dictn  = {}
    for x in testProduct:
        dictn['testDocument'] = x.testDocument
    response = flask.jsonify(dictn)
    return response


@app.route("/")
def index():
    products = pymongo.collection.Collection(databaseConfig.db, 'products')
    products.insert({'name' : 'Pallavi'})
    return '<h1>Added a User!</h1>'

if __name__ == "__main__":
    '''
        use 
            app.run(host='0.0.0.0', port=5500) to run locally. 
        
        Threaded option to enable multiple instances for multiple user access support
            app.run(threaded=True, port=5000)
    '''

    # app.run(host='0.0.0.0', port=5500)
    #from application.databaseConfig import mongo
    #import  model.productInfo as productInfo
    app.run(threaded=True, port=5000, debug=True)