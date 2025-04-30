from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import threading
import time
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:QIblI25#3@localhost/shopdb'
app.config['SECRET_KEY'] = 'dev_key'
db = SQLAlchemy(app)


initialized = False
#routes#
@app.route('/init', methods=['GET'])
def initialize():   
    
    #get the users that will be default into the database
    create_users = [
        {
            "full_name": "Admin Account",
            "email": "admin@account.com",
            "username":"Admin",  
            "user_image":"/users/character.png", #start from /images/your_file.png
            "password_hash": "admin", #we dont have hashing yet
            "user_type": "Admin" #pick one of "Admin" "Vendor" "Customer"
        },#one default user
        {
            "full_name": "Phobius Heathstone",
            "email": "pheathstone@account.com",
            "username":"Phobius",  
            "user_image":"/users/character.png", #start from /images/your_file.png
            "password_hash": "123", #we dont have hashing yet
            "user_type": "Vendor" #pick one of "Admin" "Vendor" "Customer"
        },
        
        {
            "full_name": "Player One",
            "email": "protagonist@account.com",
            "username":"Consumer",  
            "user_image":"/users/devin.png", #start from /images/your_file.png
            "password_hash": "123", #we dont have hashing yet
            "user_type": "Customer" #pick one of "Admin" "Vendor" "Customer"
        }
    ]
    for signup_data in create_users:
        if signup_data == None:
            break
        db.session.execute(text("""
                    INSERT INTO shop_user (full_name, email, username, user_image, password_hash, user_type)
                    VALUES (:full_name, :email, :username, :user_image, :password_hash, :user_type)
                """), signup_data)
    db.session.commit()
    #get the items that will be default into the database
    defaultVendor = db.session.execute(text("""
                    SELECT user_id FROM shop_user WHERE user_type = "Vendor" 
                                            """)).fetchone()
    create_items = [
        {
            "item_name":"Bastard Sword",
            "item_image":"/weapons/bastard_sword.png",#start from/images/your_file.png
            "original_price": 15,#number value
            "item_desc": "A basic arming sword",#describe the item in 200 characters or less
            "created_by": defaultVendor.user_id # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name":"Apprentice Ice Wand",
            "item_image":"/weapons/wand.png",#start from/images/your_file.png
            "original_price": 15,#number value
            "item_desc": "A basic arming sword",#describe the item in 200 characters or less
            "created_by": defaultVendor.user_id # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        }
    ]
    for create_item in create_items:
        if create_item == None:
            break
        db.session.execute(text("""
                INSERT INTO shop_item (item_name, item_image,original_price, item_desc, created_by)
                VALUES (:item_name, :item_image, :original_price, :item_desc, :created_by)
            """), create_item)
    #commit to db
    db.session.commit()
    #load homepage
    global initialized
    initialized = True
    print("Finished Initializing")
    return redirect(url_for("all_users"))
#test page to see everything!#
@app.route('/', methods=['GET', 'POST'])
def all_users():
    
    global initialized
    if initialized == False:
        firstAdmin = db.session.execute(text("SELECT email FROM shop_user WHERE user_type ='Admin' and email = 'admin@account.com'")).fetchone()
        if firstAdmin:
            initialized = True
        else:
            print("initializing")
            return redirect(url_for("initialize"))
    login = None
    admin_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Admin'")).mappings().fetchall()
    vendor_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Vendor'")).mappings().fetchall()
    customer_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Customer'")).mappings().fetchall()
    items = db.session.execute(text("SELECT * FROM shop_item")).mappings().fetchall()
    creator = db.session.execute(text("SELECT * FROM shop_user WHERE user_id = 1")).mappings().fetchone()
    cart_items = get_user_cart(session['user_id']) if 'user_id' in session else []
    order_items = get_user_order(session['user_id']) if 'user_id' in session else []
    inventory_items = get_user_inventory(session['user_id']) if 'user_id' in session else []

    
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
                           order_items=order_items,
                           inventory_items=inventory_items
                           )

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

@app.route('/to_order', methods=['GET','POST'])
def to_order():
    if request.method == 'GET':
        flash('Invalid access. Please use the cart form to submit an order.')
        return redirect(url_for('all_users'))
    if 'user_id' not in session:
        flash('Login Required')
        return redirect(url_for('all_users'))
    
    user_id = session['user_id']

    try:
        #insert orders
        db.session.execute(text("""
                           insert into shop_order (user_id, cart_id, item_id, status)
                           select :user_id, cart_id, item_id, 'Pending'
                           from shop_cart
                           where user_id = :user_id and is_ordered = false;
                           """), {'user_id':user_id})
        #then update cart!
        db.session.execute(text("""
                                update shop_cart
                                set is_ordered = true
                                where user_id = :user_id and is_ordered = false;
                                """), {'user_id':user_id})
        db.session.commit()
        flash('Order Placed!')
        return redirect(url_for('all_users'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error placeing order:{e}')
        return redirect(url_for('all_users'))
    
def get_user_order(user_id):
    return db.session.execute(text("""
    select shop_order.status,shop_item.*
    from shop_order
    join shop_item on shop_order.item_id = shop_item.item_id
    where shop_order.user_id = :user_id
"""),{'user_id':user_id}).mappings().fetchall()

@app.route('/update_order_status', methods=['POST','GET'])
def update_order_status():
     if request.method == 'GET':
        flash('Invalid access. Please use the cart form to submit an order.')
        return redirect(url_for('all_users'))
     if 'user_id' not in session:
        flash('Login Required')
        return redirect(url_for('all_users'))
     
     user_id= session['user_id']
     order_data= {
         'status':request.form['status'],
         'user_id':user_id,
         'item_id':request.form['item_id']
     }
     try:
         
         db.session.execute(text("""
                update shop_order set status = :status
                                 where user_id = :user_id and item_id = :item_id
                                 """),order_data)
         db.session.commit()
         flash('Order Updated.')
         return redirect(url_for('all_users'))
     except Exception as e:
         flash(f'Error updating order!{e}')

     return redirect(url_for('all_users'))

@app.route('/update_order_status_js', methods=['POST'])
def update_order_status_js():
    data = request.get_json()
    order_id = data.get('order_id')
    new_status = data.get('status')
    try:
        db.session.execute(text("""
                                update shop_order
                                set status = :status, last_staus_update = CURRENT_TIMESTAMP
                                where order_id = :order_id
                                """),{'status':new_status, 'order_id': order_id})
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/to_user', methods=['POST','GET'])
def to_user():
    if request.method == 'GET':
        flash('Invalid access or something.')
        return redirect(url_for('all_users'))
    if 'user_id' not in session:
        flash('login required')
        return redirect(url_for('all_users'))
    user_id = session['user_id']
    inventory_data = {
        'user_id':user_id,
        'item_id':request.form['item_id']
    }
    try:
        db.session.execute(text("""
                                insert into user_inventory(user_id, item_id, quantity)
                                values(:user_id,:item_id, 1)
                                on duplicate key update quantity = quantity + 1;
                                """),inventory_data)
        db.session.commit()
        flash('added to invertory!')
        return redirect(url_for('all_users'))
    except Exception as e:
        flash(f'Error updating Inventory: {e}')

        return redirect(url_for('all_users'))
     
def get_user_inventory(user_id):
    return db.session.execute(text("""
    select user_inventory.*,shop_item.*
    from user_inventory
    join shop_item on user_inventory.item_id = shop_item.item_id
    where user_inventory.user_id = :user_id
"""),{'user_id':user_id}).mappings().fetchall()


#this is for you to look at ronin!!!
@app.route('/equip_item/<int:item_id>', methods=['POST'])
def equip_item(item_id):
    user_id = session['user_id']
    try:
        # Unequip everything first (if needed)
        db.session.execute(text("""
            update user_inventory
            set equipped = false
            where user_id = :user_id
        """), {'user_id': user_id})

        # Equip selected item
        db.session.execute(text("""
            update user_inventory
            set equipped = true
            where user_id = :user_id and item_id = :item_id
        """), {'user_id': user_id, 'item_id': item_id})

        db.session.commit()
        flash('Item equipped!')
    except Exception as e:
        flash(f'Error equipping item: {e}')
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
    where shop_cart.user_id = :user_id and is_ordered = False
"""), {'user_id': user_id}).mappings().fetchall()
@app.route("/chat", methods=['GET','POST'])
def chat():
    user_id=session['user_id']
    _chat = db.session.execute(text(f"SELECT * FROM chat WHERE user1={user_id} OR user2={user_id}")).mappings().fetchall()
    conversation=None
    if request.form:
        if request.form["whichchat"]:
            conversation=db.session(text("SELECT conversation, comment_image,comment_date FROM message WHERE forchat=request.form['whichchat']"))
        if request.form["response"]:
            db.session.execute(text("INSERT INTO message (conversation,comment_date,userfrom,userto) VALUES(request_form['response'], NOW(), request_form['to'], request_form['from']"))
            db.session.commit()
    return render_template("chat.html",_chat=_chat, conversation=conversation)
@app.route("reviews", methods=['GET','POST'])
def reviewing():
    items=db.session.execute(text("SELECT * FROM shop_item")).all()
    if request.form:
        if request.form["object"]:
            comments=db.session.execute(text("SELECT "))
#run#
if __name__ == '__main__':
    app.run(debug=True)