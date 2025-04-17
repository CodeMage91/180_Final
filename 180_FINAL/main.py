from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:CSET115@localhost/shopdb'
app.config['SECRET_KEY'] = 'dev_key'
db = SQLAlchemy(app)

#routes#

#test page to see everything!#
@app.route('/', methods=['GET', 'POST'])
def all_users():
    admin_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Admin'")).mappings().fetchall()
    vendor_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Vendor'")).mappings().fetchall()
    customer_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Customer'")).mappings().fetchall()
    items = db.session.execute(text("SELECT * FROM shop_item")).mappings().fetchall()
    creator = db.session.execute(text("SELECT * FROM shop_user WHERE user_id = 1")).mappings().fetchone()

    if request.method == 'POST':
        if 'full_name' in request.form:  # This means the Create User form was submitted
            signup_data = {
                'full_name': request.form['full_name'],
                'email': request.form['email'],
                'username': request.form['username'],
                'password_hash': request.form['password_hash'],
                'user_type': request.form['user_type']
            }
            db.session.execute(text("""
                INSERT INTO shop_user (full_name, email, username, password_hash, user_type)
                VALUES (:full_name, :email, :username, :password_hash, :user_type)
            """), signup_data)
            db.session.commit()

        elif 'item_name' in request.form:  # This means the Create Item form was submitted
            create_item = {
                'item_name': request.form['item_name'],
                'item_image':request.form['item_image'],
                'original_price': request.form['original_price'],
                'item_desc': request.form['item_desc'],
                'created_by': 1
            }
            db.session.execute(text("""
                INSERT INTO shop_item (item_name, item_image,original_price, item_desc, created_by)
                VALUES (:item_name, :item_image, :original_price, :item_desc, :created_by)
            """), create_item)
            db.session.commit()

    return render_template('test.html',
                           admin_users=admin_users,
                           vendor_users=vendor_users,
                           customer_users=customer_users,
                           items=items,
                           creator=creator)


#run#
if __name__ == '__main__':
    app.run(debug=True)