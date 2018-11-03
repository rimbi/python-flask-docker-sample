from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import sqlalchemy as sa


# Database Configurations
app = Flask(__name__)
DATABASE = 'newtest'
PASSWORD = 'p@ssw0rd123'
USER = 'root'
HOSTNAME = 'mysqlserver'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' % (
    USER, PASSWORD, HOSTNAME, DATABASE)
db = SQLAlchemy(app)

# Database migration command line
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Exchange(db.Model):

    # Data Model User Table
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(20), unique=False)
    amount = db.Column(sa.types.Float(precision=2, scale=8), unique=False)
    price = db.Column(sa.types.Float(precision=2, scale=8), unique=False)
    final_amount = db.Column(sa.types.Float(precision=2, scale=8), unique=False)

    def __init__(self, currency, amount, price, final_amount):
        # initialize columns
        self.currency = currency
        self.amount = amount
        self.price = price
        self.final_amount = final_amount

    def __repr__(self):
        return '<Exchange %r>' % self.currency


def create_db():
    import sqlalchemy
    engine = sqlalchemy.create_engine(
        'mysql://%s:%s@%s' %
        (USER, PASSWORD, HOSTNAME))  # connect to server
    engine.execute(
        "CREATE DATABASE IF NOT EXISTS %s " %
        (DATABASE))  # create db


if __name__ == '__main__':
    manager.run()
