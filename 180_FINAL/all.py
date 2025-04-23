from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, UniqueConstraint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ------------------ MODELS ------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)  # admin, vendor, customer

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    warranty_period = db.Column(db.Date)
    colors = db.Column(db.String(200))
    size = db.Column(db.String(200))
    in_stock = db.Column(db.Integer)
    price = db.Column(db.Float)
    created_by = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)

class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    old_price = db.Column(db.Float)
    new_price = db.Column(db.Float)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    selected_color = db.Column(db.String(50))
    selected_size = db.Column(db.String(50))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date)
    total_price = db.Column(db.Float)
    status = db.Column(db.String(50))
    time = db.Column(db.DateTime)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    price_when_purchased = db.Column(db.Float)
    color = db.Column(db.String(50))
    size = db.Column(db.String(50))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    reviewer_name = db.Column(db.String(100))
    posted_date = db.Column(db.DateTime)
    index = db.Column(db.Integer)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    date = db.Column(db.DateTime)
    title = db.Column(db.String(100))
    customer_description = db.Column(db.Text)
    customer_demands = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    demand_type = db.Column(db.String(50))  # Return, Refund, Warranty
    complaint_status = db.Column(db.String(50))

class ComplaintReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    valid = db.Column(db.Boolean)
    not_valid = db.Column(db.Boolean)
    reviewed_by = db.Column(db.Integer)

class Warranty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    expiration_date = db.Column(db.Date)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reciprocate_id = db.Column(db.Integer)  # vendor/admin id

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    sender_id = db.Column(db.Integer)
    text = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ------------------ DB INIT ------------------

@app.before_first_request
def create_tables():
    db.create_all()

# ------------------ MAIN ------------------

if __name__ == '__all__':
    app.run(debug=True)
