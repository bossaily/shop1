from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Merchant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    prices = db.relationship('Price', backref='merchant', lazy=True)  # إعداد العلاقة مع Price

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    prices = db.relationship('Price', backref='product', cascade='all, delete', lazy=True)

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'), nullable=False)  # المفتاح الخارجي يشير إلى Merchant
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)    # المفتاح الخارجي يشير إلى Product
    wholesale_price = db.Column(db.Float, nullable=False)
    retail_price = db.Column(db.Float, nullable=False)