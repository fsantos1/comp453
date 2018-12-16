from flask import flask
from flask_sqlalchemy import SQLAlchemy
from flaskDemo import db
from sqlalchemy import orm, products

app = Flask(__name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///student:student@localhost/mydatabase
db = SQLAlchemy(app)


class products(db.Model):
    __tablename__= products
    ProductID = db.Column(db.Integer, primary_key=True)
    NameOfProduct = db.Column(db.String(20), unique=false, nullable=False)
    Manufacturer = db.Column(db.String(50), unique=false, nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    RAM = db.Column(db.Varchar(20), nullable=False)
    ScreenSize = db.Column(db.Varchar(20), nullable=False) 

    def __init__(self):
        return f"User('{self.ProductID}', '{self.NameOfProduct}', '{self.Manufacturer}', '{self.Price}', '{self.Price}', '{self.Price}')"


class orderdetails(db.Model):
    __tablename__= orderdetails
    OrderNumber = db.Column(db.Integer, unique=true, nullable=false)
    Price = db.Column(db.Integer, unique=false, nullable=false)
    Quantity = db.Column(db.Integer, unique=false, nullable=false)
    TotalPrice = db.Column(db.Integer, unique=false, nullable=false)
    ProductID = db.Column(db.Integer, db.ForeignKey('products.ProductID'), nullable=false)

    def__init__(self):
        return f"user('{self.OrderNumber}', '{self.Price}')"
