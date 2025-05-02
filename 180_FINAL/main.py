from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import threading
import time
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:CSET155@localhost/shopdb'
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
        },
        {
            "full_name": "Wingoul",
            "email": "flower@account.com",
            "username":"Dippi",  
            "user_image":"/users/wingall_img", #start from /images/your_file.png
            "password_hash": "123", #we dont have hashing yet
            "user_type": "Vendor" #pick one of "Admin" "Vendor" "Customer"
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
    vendors = db.session.execute(text("""
                    SELECT user_id FROM shop_user WHERE user_type = "Vendor" 
                                            """)).mappings().fetchall()
    print(vendors)
    create_items = [
        {
            "item_name":"Bastard Sword",
            "item_image":"/weapons/bastard_sword.png",#start from/images/your_file.png
            "original_price": 15,#number value
            "item_desc": "A basic arming sword",#describe the item in 200 characters or less
            "created_by": 0 # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name":"Apprentice Ice Wand",
            "item_image":"/weapons/wand.png",#start from/images/your_file.png
            "original_price": 15,#number value
            "item_desc": "A basic arming sword",#describe the item in 200 characters or less
            "created_by": 0 # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Health Potion",
            "item_image": "/items/health_potion.png",  # start from/images/your_file.png
            "original_price": 25,  # number value
            "item_desc": "A reinvigorating magical potion that mends your wounds, ameliorates your pain, and restores your vigor. Heals your HP by 30 points.",
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Iron Sword",
            "item_image": "/weapons/iron_bladed_weapon.png",  # start from/images/your_file.png
            "original_price": 100,  # number value
            "item_desc": "A simple iron blade that will prove proficient in dispatching your foes. Deals 80 points of damage.",
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Throwable Acid Potion",
            "item_image": "/items/throwable_acid_potion.png",  # start from/images/your_file.png
            "original_price": 15,  # number value
            "item_desc": "This toxic magical concoction is excellent at burning your opponents with acidic liquid. Does 10 points of damage on hot, and 1 point of damage per second for the next 10 seconds.",
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Guinness",
            "item_image": "/items/Guinness_(1).png",  # start from/images/your_file.png
            "original_price": 5,  # number value
            "item_desc": "A refreshing liquor, whether your 1% Irish or 99% Irish.",
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Iron Mace",
            "item_image": "/weapons/iron_mace.png",  # start from/images/your_file.png
            "original_price": 100,  # number value
            "item_desc": "A well-forged bludgeon made of fine steel, perfect for discombobulating your opponents. Deals 50 points of damage, with a 25% chance to stun your target.",
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Poisoned Throwing Knife",
            "item_image": "/weapons/poisoned_throwing_knife.png",  # start from/images/your_file.png
            "original_price": 30,  # number value
            "item_desc": "A small iron dagger, this dimunitive blade compensates for its small size with a nasty coating of acid. Deals 15 points of damage on hit, and does 2 points of damage every second.",
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Mithril Sword",
            "item_image": "/weapons/mithril_bladed_weapon.png",  # start from/images/your_file.png
            "original_price": 200,  # number value
            "item_desc": "A blade forged from the ore of legends, this mighty sword will prove beyond capable of vanquishing your foes. Deals 120 points of damage",
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Bomb",
            "item_image": "/weapons/Bomb.png",  # start from/images/your_file.png
            "original_price": 75,  # number value
            "item_desc": "Alongside lamp-oil and rope, these explosive weapons are a must-have for adventurers. Deals 80 points of damage per hit.",
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Potion of Draconic Strength",
            "item_image": "/items/potion_of_draconic_strength.png",  # start from/images/your_file.png
            "original_price": 80,  # number value
            "item_desc": "Brewed by the dragons to help other species, this fiery and sweet magical elixir grants the drinker strength verging on that of the dragons themselves. Gives the player a 100 point melee damage buff.",
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        }
    ]
    vendorNum = 0
    for i, item in enumerate(create_items):
        if i % 5 == 0:
            vendorNum+=1
        if vendorNum == len(vendors):
            vendorNum = 0
        vendor = vendors[vendorNum]
        item["created_by"] = vendor["user_id"]
    
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
    session['user_id'] = None
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
    if session['user_id']:
        login = db.session.execute(text("SELECT * FROM shop_user WHERE user_id = :user_id"), {"user_id": session["user_id"]}).first()
    admin_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Admin'")).mappings().fetchall()
    vendor_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Vendor'")).mappings().fetchall()
    customer_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Customer'")).mappings().fetchall()
    items = db.session.execute(text("SELECT * FROM shop_item")).mappings().fetchall()
    creator = db.session.execute(text("SELECT * FROM shop_user WHERE user_id = 1")).mappings().fetchone()
    cart_items = get_user_cart(session['user_id']) if 'user_id' in session else []
    order_items = get_user_order(session['user_id']) if 'user_id' in session else []
    inventory_items = get_user_inventory(session['user_id']) if 'user_id' in session else []
    battle = False
    
    if request.method == 'POST':
        if 'full_name' in request.form:  # This means the Create User form was submitted
            signup_data = {
                'full_name': request.form['full_name'],
                'email': request.form['email'],
                'username': request.form['username'],
                'password_hash': generate_password_hash(request.form['password_hash']),
                'user_type': request.form['user_type']
            }

            if 'user_image' in request.form and request.form['user_image']:
                signup_data['user_image'] = request.form['user_image']
            else:
                signup_data['user_image'] = 'blue_guy_idle_gif.gif'

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


    return render_template('battle.html',
                           admin_users=admin_users,
                           vendor_users=vendor_users,
                           customer_users=customer_users,
                           items=items,
                           creator=creator,
                           login=login,
                           cart_items=cart_items,
                           order_items=order_items,
                           inventory_items=inventory_items,
                           battle=battle
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
    print(session.items())
    for key in session.keys():
        session[key] = None
    print(session.items())
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
        if "whichchat" in request.form:
            conversation=db.session.execute(text(f"SELECT * FROM message WHERE forchat={request.form["whichchat"]}")).mappings().fetchall()
        if "response" in request.form:
            chatid=db.session.execute(text(f"SELECT * FROM chat WHERE (user1={request.form["to"]} AND user2={request.form["as"]}) OR (user1={request.form["as"]} AND user2={request.form["to"]})")).first()
            if chatid==None:
                db.session.execute(text(f"INSERT INTO chat (user1, user2) VALUES ({request.form["as"]},{request.form["to"]}"))
            db.session.execute(text(
                f"INSERT INTO message (forchat,conversation,comment_date,from_user,to_user) VALUES({chatid.chatid},'{request.form['response']}', NOW(), {request.form['as']}, {request.form['to']})"))
            db.session.commit()

    return render_template("chat.html",_chat=_chat, conversation=conversation)
@app.route("/reviews", methods=['GET','POST'])
def reviewing():
    items=db.session.execute(text("SELECT * FROM shop_item")).all()
    comments=None
    if request.form:
        user_id=session['user_id']
        if "object" in request.form:
            comments=db.session.execute(text(f"SELECT rating, statement, review_image, review_date FROM review WHERE for_item={request.form['object']}")).all()
        if "review" in request.form:
            db.session.execute(text(f"INSERT INTO review (from_user,for_item,rating,review_date,statement) VALUES ({user_id},{request.form['iditem']},{request.form["rating"]}, NOW(),'{request.form["review"]}')"))
            db.session.commit()
    return render_template("reviews.html", items=items,comments=comments)
#run#
if __name__ == '__main__':
    app.run(debug=True)