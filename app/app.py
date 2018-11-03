from __future__ import print_function
from flask import Flask
from flask import request
from flask import request
from flask_restful import Resource, Api, abort
from model import create_db
from model import db
from model import Exchange
from model import app as application
import requests
import simplejson as json
from sqlalchemy.exc import IntegrityError
import os

# initate flask app
app = Flask(__name__)
api = Api(app)


class LastExchanges(Resource):
    def get(self):
        """
        Returns last <n> operations
        """
        try:
            exchanges = self.modify_query(
                Exchange.query.order_by(
                    Exchange.id.desc()))
            # exchanges = Exchange.query.filter_by(currency=currency).first_or_404()
            exchanges_dict = {}
            # for exchange in exchanges:
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

    def modify_query(self, query):
        return query


class LastNExchanges(LastExchanges):
    def get(self, n):
        """
        Returns last <n> operations
        """
        self.n = n
        return super(LastNExchanges, self).get()

    def modify_query(self, query):
        return query.limit(self.n)


class LastExchange(LastNExchanges):
    def get(self):
        """
        Returns last  exchange
        """
        return super(LastExchange, self).get(1)


class LastExchangeByCurrency(LastExchange):
    def get(self, currency):
        """
        Returns last  exchanges of the <currency>
        """
        self.currency = currency
        return super(LastExchangeByCurrency, self).get()

    def modify_query(self, query):
        query = query.filter_by(currency=self.currency)
        return super(LastExchangeByCurrency, self).modify_query(query)


class LastNExchangesByCurrency(LastNExchanges):
    def get(self, currency, n):
        """
        Returns last <n> operations
        """
        self.currency = currency
        return super(LastNExchangesByCurrency, self).get(n)

    def modify_query(self, query):
        query = query.filter_by(currency=self.currency)
        return super(LastNExchangesByCurrency, self).modify_query(query)


class ExchangeList(Resource):
    def get(self):
        """
        Returns all exchanges
        """
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
        """
        Processes and saves an exchange request
        """
        try:
            data = request.get_json(force=True)
            resp = requests.get(
                'https://openexchangerates.org/api/latest.json?app_id=841a28ce9a464522bae12e9001d22ec8')
            import sys
            print(resp.json()['rates'], file=sys.stderr)
            if resp.status_code != 200:
                abort(404, message="Exchange rate info not accessible")
            service_data = resp.json()
            currency = data['currency'].upper()
            amount = data['amount']
            if currency not in service_data['rates']:
                abort(404, message="This exchange is not supported")
            price = service_data['rates'][currency]
            final_amount = amount / price
            print(currency, amount, price, final_amount, file=sys.stderr)
            exchange = Exchange(currency,
                                amount,
                                price,
                                final_amount)
            db.session.add(exchange)
            db.session.commit()
            return json.dumps({'status': True})
        except IntegrityError:
            return json.dumps({'status': False})


api.add_resource(ExchangeList, '/grab_and_save')
api.add_resource(LastExchange, '/last')
api.add_resource(LastExchangeByCurrency, '/last/<string:currency>')
api.add_resource(LastNExchanges, '/last/<int:n>')
api.add_resource(LastNExchangesByCurrency, '/last/<string:currency>/<int:n>')


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
    # TODO: Find a real solution to this problem
    import time
    time.sleep(5)
    create_db()
    create_tables()
    app.run(host="0.0.0.0", port=8082, debug=True)
