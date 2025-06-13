from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, unique=True, nullable=False)
    full_name = db.Column(db.String(120))
    username = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Listing(db.Model):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    region = db.Column(db.String(50))  
    city = db.Column(db.String(100))  
    bedrooms = db.Column(db.Integer)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_urls = db.Column(db.Text)
    contact = db.Column(db.Text)
