from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:CSET155@localhost/shopdb'
app.config['SECRET_KEY'] = 'dev_key'
db = SQLAlchemy(app)

#routes#

#test page to see everything!#
@app.route('/', methods=['GET', 'POST'])
def all_users():
    login = None
    object_data = []

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
                'user_image': request.form['user_image'],
                'password_hash': request.form['password_hash'],
                'user_type': request.form['user_type']
            }
            db.session.execute(text("""
                INSERT INTO shop_user (full_name, email, username, user_image, password_hash, user_type)
                VALUES (:full_name, :email, :username, :user_image, :password_hash, :user_type)
            """), signup_data)
            db.session.commit()

        elif 'login_email' in request.form: #This means user is logining in.
            email = request.form['login_email']
            password_hash = request.form['password_hash']

            login_data = db.session.execute(text("""
                select * from shop_user where email = :e and password_hash = :p
            """), {'e': email, 'p': password_hash}).mappings().fetchone()

            if login_data:
                session['user_id'] = login_data['user_id']

                #where's mah wallet
                wallet_data = db.session.execute(text("""
                    select * from shop_wallet where user_id = :user_id
                """), {'user_id': login_data['user_id']}).mappings().fetchone()

                cart_data = db.session.execute(text("""
                    select * from shop_cart where user_id = :user_id
                """), {'user_id': login_data['user_id']}).mappings().fetchone()

                if cart_data:
                    object_data = db.session.execute(text("""
                        SELECT si.item_name, si.item_desc, si.original_price
                        FROM cart_object co
                        JOIN shop_item si ON co.item_id = si.item_id
                        WHERE co.cart_id = :cart_id
                    """), {'cart_id': cart_data['cart_id']}).mappings().fetchall()

                if login_data:
                    login_data = dict(login_data)
                    if cart_data:
                        login_data['cart_id'] = cart_data['cart_id']
                        login_data['cart_total'] = cart_data['cart_total']

                    #Merge wallet into login
                    if wallet_data:
                        login_data['wallet_amount'] = wallet_data['wallet_amount']

                    login = login_data
                    flash('login success!', 'success')
            else:
                flash('Invalid email or password')

        elif 'add_item_id' in request.form:
            if 'user_id' not in session:
                flash("You must be logged in to add to cart", "error")
            else:
                user_id = session['user_id']
                item_id = request.form['add_item_id']

                # Get or create cart
                cart_data = db.session.execute(text("""
                    SELECT * FROM shop_cart WHERE user_id = :user_id
                """), {'user_id': user_id}).mappings().fetchone()

                if not cart_data:
                    # create cart if it doesn't exist
                    db.session.execute(text("""
                        INSERT INTO shop_cart (user_id, cart_total)
                        VALUES (:user_id, 0)
                    """), {'user_id': user_id})
                    db.session.commit()

                    cart_data = db.session.execute(text("""
                        SELECT * FROM shop_cart WHERE user_id = :user_id
                    """), {'user_id': user_id}).mappings().fetchone()

                if cart_data:
                    # Add item to cart_object
                    db.session.execute(text("""
                        INSERT INTO cart_object (cart_id, item_id)
                        VALUES (:cart_id, :item_id)
                    """), {'cart_id': cart_data['cart_id'], 'item_id': item_id})

                    # Get the item price
                    item_price = db.session.execute(text("""
                        SELECT original_price FROM shop_item WHERE item_id = :item_id
                    """), {'item_id': item_id}).scalar()

                    if item_price is not None:
                        # Update the cart total
                        new_total = cart_data['cart_total'] + float(item_price)
                        db.session.execute(text("""
                            UPDATE shop_cart SET cart_total = :total WHERE cart_id = :cart_id
                        """), {'total': new_total, 'cart_id': cart_data['cart_id']})
                        db.session.commit()
                        flash("Item added to cart!", "success")
                    else:
                        flash("Error: Item price not found.", "error")
                else:
                    flash("Error: Could not retrieve or create cart.", "error")

        elif 'item_name' in request.form:  # This means the Create Item form was submitted
            item_name = request.form.get('item_name')
            item_image = request.form.get('item_image')
            original_price_str = request.form.get('original_price')
            item_desc = request.form.get('item_desc')

            # Validate and convert original_price
            try:
                original_price = float(original_price_str) if original_price_str else None
            except ValueError:
                flash("Invalid price format. Please enter a number.", "error")
                return redirect(url_for('all_users')) # Redirect to prevent insertion

            if original_price is not None:
                create_item = {
                    'item_name': item_name,
                    'item_image': item_image,
                    'original_price': original_price,
                    'item_desc': item_desc,
                    'created_by': 1
                }
                db.session.execute(text("""
                    INSERT INTO shop_item (item_name, item_image, original_price, item_desc, created_by)
                    VALUES (:item_name, :item_image, :original_price, :item_desc, :created_by)
                """), create_item)
                db.session.commit()
                flash("Item created successfully!", "success")
            else:
                flash("Price cannot be empty.", "error")
                return redirect(url_for('all_users')) # Redirect to prevent insertion

    return render_template('test.html',
                           admin_users=admin_users,
                           vendor_users=vendor_users,
                           customer_users=customer_users,
                           items=items,
                           creator=creator,
                           login=login,
                           object_data=object_data)


#run#
if __name__ == '__main__':
    app.run(debug=True)