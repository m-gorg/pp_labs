from flask import Flask
from sqlalchemy.orm.session import sessionmaker
from Database_model import engine

app = Flask(__name__)
app.testing = True
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

from methods import api_blueprint
app.register_blueprint(api_blueprint)
