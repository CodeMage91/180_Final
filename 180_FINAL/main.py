from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:CSET155@localhost/shopdb'
app.config['SECRET_KEY'] = 'dev_key'
db = SQLAlchemy(app)

#routes#

#test page to see everything!#
@app.route('/', methods=['GET', 'POST'])
def all_users():
    login = None
    admin_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Admin'")).mappings().fetchall()
    vendor_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Vendor'")).mappings().fetchall()
    customer_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Customer'")).mappings().fetchall()
    items = db.session.execute(text("SELECT * FROM shop_item")).mappings().fetchall()
    creator = db.session.execute(text("SELECT * FROM shop_user WHERE user_id = 1")).mappings().fetchone()
    cart_items = get_user_cart(session['user_id']) if 'user_id' in session else []
    order_items = get_user_order(session['user_id']) if 'user_id' in session else []

    if request.method == 'POST':
        if 'full_name' in request.form:  # This means the Create User form was submitted
            signup_data = {
                'full_name': request.form['full_name'],
                'email': request.form['email'],
                'username': request.form['username'],
                'user_image':request.form['user_image'],
                'password_hash': generate_password_hash(request.form['password_hash']),
                'user_type': request.form['user_type']
            }
            db.session.execute(text("""
                INSERT INTO shop_user (full_name, email, username, user_image, password_hash, user_type)
                VALUES (:full_name, :email, :username, :user_image, :password_hash, :user_type)
            """), signup_data)
            db.session.commit()



            #login stuff

        elif 'login_email'in request.form: #This means user is logining in.
             email =request.form['login_email']
             password_hash = request.form['password_hash']

             login_data = db.session.execute(text("""
            select * from shop_user where email = :e and password_hash = :p
            """), {'e':email, 'p': password_hash}).mappings().fetchone()
             
             
             if login_data:
                 session['user_id'] = login_data['user_id']
                 
                                                                 #where's mah wallet
              
                 
                 
                 login = login_data
                 flash('login success!')
                 return redirect(url_for('all_users'))
             else:
                flash('Invalid email or password')
              
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
                           creator=creator,
                           login=login,
                           cart_items=cart_items,
                           order_items=order_items)

@app.route('/to_cart/', methods=['POST'])
def to_cart():
     if 'user_id' not in session:
         flash('Login required!')
         return redirect(url_for('all_users'))


     user_id = session['user_id'] 
   
     cart_data = {
             'user_id':user_id,
             'item_id':request.form['item_id']
         }
     db.session.execute(text("""
                insert into shop_cart(user_id,item_id)
                                 values(:user_id,:item_id)
                                """),cart_data)
     db.session.commit()
     return redirect(url_for('all_users'))

@app.route('/submit_order', methods=['POST'])
def submit_order():
    if 'user_id' not in session:
        flash('Login Required!')
        return redirect(url_for('all_users'))
    user_id = session['user_id']
    order_data = {
        'user_id':user_id,
        'cart_id':request.form['cart_id'],
        'item_id':request.form['item_id'],
        'status':request.form['status']
    }
    db.session.execute(text("""
insert into shop_order(user_id,cart_id,item_id,status)
    values(:user_id,:cart_id,:item_id,:status)
"""),order_data)
    db.session.commit()
    return redirect(url_for('all_users'))


@app.route('/logout')
def logout():
    session.clear()
    flash('logged out.','info')
    return redirect(url_for('all_users'))

def get_user_cart(user_id):
    return db.session.execute(text("""
    select shop_item.*
    from shop_cart
    join shop_item on shop_cart.item_id = shop_item.item_id
    where shop_cart.user_id = :user_id
"""), {'user_id': user_id}).mappings().fetchall()

def get_user_order(user_id):
    return db.session.execute(text("""
    select shop_order.*,shop_item.*
    from shop_order
    join shop_item on shop_order.item_id = shop_item.item_id
    where shop_order.user_id = :user_id
"""),{'user_id':user_id}).mappings().fetchall()

def get_user_cart(user_id):
    return db.session.execute(text("""
    SELECT shop_cart.cart_id, shop_item.*
    FROM shop_cart
    JOIN shop_item ON shop_cart.item_id = shop_item.item_id
    WHERE shop_cart.user_id = :user_id
    """), {'user_id': user_id}).mappings().fetchall()




#run#
if __name__ == '__main__':
    app.run(debug=True)