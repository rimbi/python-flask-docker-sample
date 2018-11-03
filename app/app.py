from __future__ import print_function
from flask import Flask
from flask import request
from flask import request
from flask_restful import Resource, Api
from model import create_db
from model import db
from model import Exchange
from model import app as application
import simplejson as json
from sqlalchemy.exc import IntegrityError
import os

# initate flask app
app = Flask(__name__)
api = Api(app)


class ExchangeResource(Resource):
    def get(self, currency):
        try:
            exchanges = Exchange.query.filter_by(currency=currency).first_or_404()
            exchanges_dict = {}
            for exchange in exchanges:
                exchanges_dict[exchange.id] = {
                    'currency': exchange.currency,
                    'amount': exchange.amount,
                    'price': exchange.price,
                    'final_amount': exchange.final_amount
                }
    
            return json.dumps(exchanges_dict)
        except IntegrityError:
            return json.dumps({})


class ExchangeListResource(Resource):
    def get(self):
        try:
            exchanges = Exchange.query.all()
            exchanges_dict = {}
            for exchange in exchanges:
                exchanges_dict[exchange.id] = {
                    'currency': exchange.currency,
                    'amount': exchange.amount,
                    'price': exchange.price,
                    'final_amount': exchange.final_amount
                }
    
            return json.dumps(exchanges_dict)
        except IntegrityError:
            return json.dumps({})

    def post(self):
        try:
            data = request.get_json(force=True)
            exchange = Exchange(data['currency'],
                            data['amount'],
                            data['price'],
                            data['final_amount'])
            db.session.add(exchange)
            db.session.commit()
            return json.dumps({'status': True})
        except IntegrityError:
            return json.dumps({'status': False})


api.add_resource(ExchangeListResource, '/exchanges')
api.add_resource(ExchangeResource, '/exchanges/<currency>')


def create_tables():
    """
    Create tables on the db
    """
    try:
        db.create_all()
        return True
    except IntegrityError:
        return False


# run app service
if __name__ == "__main__":
    import time
    time.sleep(5)
    create_db()
    create_tables()
    app.run(host="0.0.0.0", port=8082, debug=True)
