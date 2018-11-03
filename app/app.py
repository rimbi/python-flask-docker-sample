from __future__ import print_function
from flask import Flask
from flask import request
from flask import request
from flask_restful import Resource, Api
from model import create_db
from model import db
from model import User
from model import app as application
import simplejson as json
from sqlalchemy.exc import IntegrityError
import os

# initate flask app
app = Flask(__name__)
api = Api(app)


class UserResource(Resource):
    def get(self, username):
        # return json.dumps({'username':request.args['username']})
        try:
            user = User.query.filter_by(username=username).first_or_404()
            return json.dumps(
                {user.username: {'email': user.email, 'phone': user.phone, 'fax': user.fax}})
        except IntegrityError:
            return json.dumps({})


class UserListResource(Resource):
    def get(self):
        try:
            users = User.query.all()
            users_dict = {}
            for user in users:
                users_dict[user.username] = {
                    'email': user.email,
                    'phone': user.phone,
                    'fax': user.fax
                }
    
            return json.dumps(users_dict)
        except IntegrityError:
            return json.dumps({})

    def post(self):
        try:
            import sys
            print('Deneme', file=sys.stderr)
            data = request.get_json(force=True)
            user = User(data['username'],
                        data['email'],
                        data['phone'],
                        data['fax'])
            db.session.add(user)
            db.session.commit()
            return json.dumps({'status': True})
        except IntegrityError:
            return json.dumps({'status': False})


api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<username>')


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
