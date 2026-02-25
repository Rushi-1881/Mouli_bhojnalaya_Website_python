from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the db object
db = SQLAlchemy()

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(500), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(50), default="Cash on Delivery")
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    order_details = db.Column(db.Text, nullable=False)