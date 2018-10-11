from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:st!xadminHY@11.11.11.9/crmApiUser'
db = SQLAlchemy(app)
from my_app.dbStructure.dbStructure import User
db.create_all()