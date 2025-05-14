from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import threading
import time
import math
from datetime import datetime, timedelta, date


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
            "user_image":"/users/wingall_img.png", #start from /images/your_file.png
            "password_hash": "123", #we dont have hashing yet
            "user_type": "Vendor" #pick one of "Admin" "Vendor" "Customer"
        },
        {
            "full_name": "Lucius Augustus Kaiser",
            "email": "emperor@account.com",
            "username":"Kaiser",  
            "user_image":"/vendor_03.png", #start from /images/your_file.png
            "password_hash": "123", #we dont have hashing yet
            "user_type": "Vendor" #pick one of "Admin" "Vendor" "Customer"   
        }
    ]
    for signup_data in create_users:
        if signup_data == None:
            break
        if 'user_image_small' not in signup_data:
            signup_data['user_image_small'] = '/users/small_blue_boi_00.gif'
        db.session.execute(text("""
                    INSERT INTO shop_user (full_name, email, username, user_image,user_image_small,password_hash, user_type)
                    VALUES (:full_name, :email, :username, :user_image, :user_image_small, :password_hash, :user_type)
                """), signup_data)
    db.session.commit()
    #adding initial money to the protagonist account
    db.session.execute(text("update shop_user set balance = 200 where full_name = 'Player One'"))
    db.session.commit()
    #get the items that will be default into the database
    vendors = db.session.execute(text("""
                    SELECT user_id, full_name FROM shop_user WHERE user_type = "Vendor" 
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
            "item_desc": "A basic wand tied to ice elemental magic.",#describe the item in 200 characters or less
            "created_by": 0 # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Health Potion",
            "item_image": "/items/health_potion.png",  # start from/images/your_file.png
            "original_price": 25,  # number value
            "item_desc": "A magical potion that mends your wounds.", # heals 30 points
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Iron Sword",
            "item_image": "/weapons/iron_bladed_weapon.png",  # start from/images/your_file.png
            "original_price": 100,  # number value
            "item_desc": "A simple iron blade that will prove proficient in dispatching your foes.",#80 damage
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Throwable Acid Potion",
            "item_image": "/items/throwable_acid_potion.png",  # start from/images/your_file.png
            "original_price": 15,  # number value
            "item_desc": "This toxic magical concoction is excellent at burning your opponents.", #10 points on hit, 1 per second for 5 seconds
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
            "item_desc": "A well-forged bludgeon made of fine steel.", #50 damage, 25% chance to stun
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Poisoned Throwing Knife",
            "item_image": "/weapons/poisoned_throwing_knife.png",  # start from/images/your_file.png
            "original_price": 30,  # number value
            "item_desc": "A small iron dagger with a nasty coating of acid.", # 15 damage on hit, 2 damage every 1 second for 10 seconds
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Mithril Sword",
            "item_image": "/weapons/mithril_bladed_weapon.png",  # start from/images/your_file.png
            "original_price": 200,  # number value
            "item_desc": "A mithril blade adept at dispatching your opponents.", #120 damage
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Bomb",
            "item_image": "/weapons/Bomb.png",  # start from/images/your_file.png
            "original_price": 75,  # number value
            "item_desc": "An incredibly destructive explosive weapon.", # 80 damage
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Potion of Draconic Strength",
            "item_image": "/items/potion_of_draconic_strength.png",  # start from/images/your_file.png
            "original_price": 80,  # number value
            "item_desc": "Gives you dragon-like strength.", # 100 point melee damage buff
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name":"Starter Sword",
            "item_image":"/weapons/sword_00.png",#start from/images/your_file.png
            "original_price": 5,#number value
            "item_desc": "Balanced in weight, swift like a branch.",#describe the item in 200 characters or less
            "created_by": 14 # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
        "item_name":"Starter Staff",
            "item_image":"/weapons/staff_00.png",#start from/images/your_file.png
            "original_price": 5,#number value
            "item_desc": "Surprisingly sturdy and weighted.",#describe the item in 200 characters or less
            "created_by": 14 # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
        "item_name":"Starter Mace",
            "item_image":"/weapons/mace_00.png",#start from/images/your_file.png
            "original_price": 5,#number value
            "item_desc": "This was made for smashing, it lands with a thud.",#describe the item in 200 characters or less
            "created_by": 14 # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Leather Armor",
            "item_image": "/equipment/leather_armor.png",  # start from/images/your_file.png
            "original_price": 80,  # number value
            "item_desc": "A simple set of leather armor, studded with metal.", #25 defensive points
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Chainmail Armor",
            "item_image": "/equipment/chainmail_armor.png",  # start from/images/your_file.png
            "original_price": 120,  # number value
            "item_desc": "A protective mesh suit.", #50 defensive points
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Iron Armor",
            "item_image": "/equipment/iron_armor.png",  # start from/images/your_file.png
            "original_price": 200,  # number value
            "item_desc": "A set of iron plated armor.", # 75 defensive points
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Mithril Chain Shirt",
            "item_image": "/equipment/mithril_chain_shirt.png",  # start from/images/your_file.png
            "original_price": 280,  # number value
            "item_desc": "A rare mithril chain shirt", # 100 defensive points
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Mithril Plate Armor",
            "item_image": "/equipment/mithril_armor.png",  # start from/images/your_file.png
            "original_price": 350,  # number value
            "item_desc": "An expensive and durable set of mithril plate armor.", # 200 points of defensive armor
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Mithril Plate Armor",
            "item_image": "/equipment/mithril_armor.png",  # start from/images/your_file.png
            "original_price": 350,  # number value
            "item_desc": "An expensive and durable set of mithril plate armor.", # 200 points of defensive armor
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Starter Shield",
            "item_image": "/icons/icon_13.png",  # start from/images/your_file.png
            "original_price": 1350,  # number value
            "item_desc": "This shield is perfect for new adventurers that prioritize defense over maneverability.", 
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
            "item_name": "Merri Potion",
            "item_image": "/icons/icon_02.png",  # start from/images/your_file.png
            "original_price": 1200,  # number value
            "item_desc": "A potion that will heal all injuries and bring you to perfect health.", 
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
        "item_name": "Tasty Ether",
            "item_image": "/icons/icon_08.png",  # start from/images/your_file.png
            "original_price": 1200,  # number value
            "item_desc": "A fizzy drink that leaves you feeling magical.", 
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
        "item_name": "Fresh Swifties",
            "item_image": "/icons/icon_09.png",  # start from/images/your_file.png
            "original_price": 1200,  # number value
            "item_desc": "A pair of shoes that allow you to move swiftly.", 
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
        "item_name": "Hardy Hat",
            "item_image": "/icons/icon_11.png",  # start from/images/your_file.png
            "original_price": 1200,  # number value
            "item_desc": "A hat that gives you a little bit of confidence and boost you max health.", 
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        },
        {
        "item_name": "Rabbits Foot",
            "item_image": "/icons/icon_12.png",  # start from/images/your_file.png
            "original_price": 1200,  # number value
            "item_desc": "This lucky charm is supposed to be lucky.", 
            # describe the item in 200 characters or less
            "created_by": 0  # USER ID! BE SPECIFIC DO NOT MESS UP WHO IT WAS CREATED BY
        }
    ]
    
    phobius = None
    for i in vendors:
        if i['full_name'] == "Phobius Heathstone":
            phobius = i
            break
    vendorNum = 0
    for i, item in enumerate(create_items):
        if i % 5 == 0:
            vendorNum+=1
        if vendorNum == len(vendors):
            vendorNum = 0
        vendor = vendors[vendorNum]
        item["created_by"] = phobius['user_id']
    for create_item in create_items:
        if create_item == None:
            break
        db.session.execute(text("""
                INSERT INTO shop_item (item_name, item_image,original_price, item_desc, created_by)
                VALUES (:item_name, :item_image, :original_price, :item_desc, :created_by)
            """), create_item)
    #commit to db
    db.session.commit()
    item_stat_blocks = {
        "Bastard Sword":         {"STR": 5,  "DEX": 1},
        "Apprentice Ice Wand":   {"INTEL": 4},
        "Health Potion":         {"CON": 2},
        "Iron Sword":            {"STR": 8},
        "Throwable Acid Potion": {"INTEL": 2, "DEX": 2},
        "Guinness":              {"CHA": 3, "LUCK": 1},
        "Iron Mace":             {"STR": 6, "LUCK": 1},
        "Poisoned Throwing Knife": {"DEX": 4, "LUCK": 2},
        "Mithril Sword":         {"STR": 10, "DEX": 2},
        "Bomb":                  {"STR": 5, "INTEL": 3},
        "Potion of Draconic Strength": {"STR": 15, "CON": 5},
        "Starter Sword":         {"STR": 1, "DEX": 1},
        "Starter Staff":         {"INTEL": 1, "WIS": 1},
        "Starter Mace":          {"STR": 2},
        "Leather Armor":         {"CON": 3},
        "Chainmail Armor":       {"CON": 5},
        "Iron Armor":            {"CON": 8},
        "Mithril Chain Shirt":   {"CON": 12},
        "Mithril Plate Armor":   {"CON": 20}
    }
    items = db.session.execute(text('select * from shop_item')).mappings().fetchall()
    for key, stat in item_stat_blocks.items():
        for item in items:
            if item.item_name == key:
                stat_data = {
                    "item_id": item.item_id,
                    "item_name": item.item_name,
                    "STR": stat.get("STR", 0),
                    "DEX": stat.get("DEX", 0),
                    "CON": stat.get("CON", 0),
                    "INTEL": stat.get("INTEL", 0),
                    "CHA": stat.get("CHA", 0),
                    "WIS": stat.get("WIS", 0),
                    "LUCK": stat.get("LUCK", 0)
                }
                db.session.execute(text("""
                    INSERT INTO item_stats (item_id, item_name, STR, DEX, CON, INTEL, CHA, WIS, LUCK)
                    VALUES (:item_id, :item_name, :STR, :DEX, :CON, :INTEL, :CHA, :WIS, :LUCK)
                """), stat_data)
                continue
    #commit to db
    db.session.commit()
    #load homepage
    global initialized
    initialized = True
    session['user_id'] = None
    print("Finished Initializing")
    return redirect(url_for("all_users"))
#page to see everything!#
@app.route('/', methods=['GET', 'POST'])
def all_users():
    if 'html' not in session:
        session['html'] = 'battle.html'
    html = session['html']
    if 'user_id' not in session:
        session['user_id'] = None
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
    users = db.session.execute(text("SELECT * FROM shop_user")).mappings().fetchall()
    admin_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Admin'")).mappings().fetchall()
    vendor_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Vendor'")).mappings().fetchall()
    customer_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Customer'")).mappings().fetchall()
    items = db.session.execute(text("SELECT * FROM shop_item")).mappings().fetchall()
    creator = db.session.execute(text("SELECT * FROM shop_user WHERE user_id = 1")).mappings().fetchone()
    cart_items = get_user_cart(session['user_id']) if 'user_id' in session else []
    cart_total = db.session.execute(text("SELECT sum(item.original_price) as 'cart_total' from shop_cart cross join shop_item as item where shop_cart.item_id = item.item_id and is_ordered = false and user_id = :user_id"), {"user_id": session["user_id"]}).first()
    order = get_user_order(session['user_id'], None) if 'user_id' in session else []
    all_carts = get_all_carts()
    if session['user_id']:
        print('user')
        for vendor in vendor_users:
            print(vendor,'vendor')
            if session['user_id'] ==  vendor['user_id']:
                order = get_user_order(None, session['user_id']) 
                print(order)
                break
        for admin in admin_users:
            if session['user_id'] ==  admin['user_id']:
                order = get_user_order(None, None) 
                print(order)
                break
    user_order = order[0]
    order_items = order[1]
    inventory_items = get_user_inventory(session['user_id']) if 'user_id' in session else []
    print(inventory_items, 'hui')
    battle = False
    print(html)
    
    if request.method == 'POST':
        if 'full_name' in request.form:  # This means the Create User form was submitted
            signup_data = {
                'full_name': request.form['full_name'],
                'email': request.form['email'],
                'username': request.form['username'],
                'password_hash': request.form['password_hash'],
                'user_type': request.form['user_type']
            }
            if 'user_image' in request.form and request.form['user_image']:
                signup_data['user_image'] = request.form['user_image']
            else:
                signup_data['user_image'] = 'users/blue_guy_idle_gif.gif'

            if 'user_image_small' in request.form and request.form['user_image_small']:
                signup_data['user_image_small'] = request.form['user_image_small']
            else:
                signup_data['user_image_small'] = '/users/small_blue_boi.png'

            db.session.execute(text("""
                INSERT INTO shop_user (full_name, email, username, user_image, user_image_small, password_hash, user_type)
                VALUES (:full_name, :email, :username, :user_image, :user_image_small, :password_hash, :user_type)
            """), signup_data)

            
            db.session.commit()

            user_result = db.session.execute(text("SELECT user_id FROM shop_user WHERE username = :username"), {'username': signup_data['username']})
            user_id = user_result.fetchone()[0]

            starter_weapon_id = request.form.get('starter_weapon_id') or '6'#default weapon sword
            starter_weapon = {
                'user_id': user_id,
                'item_id': starter_weapon_id
            }

            starter_gift_id = request.form.get('starter_gift_id') or '26'#default gift rabbits foot
            gift_item = {
                'user_id':user_id,
                'item_id':starter_gift_id
            }
 
            db.session.execute(text("""
                INSERT INTO user_inventory (user_id,item_id)
                VALUES (:user_id,:item_id)
                                    """),starter_weapon)
            
            db.session.execute(text("""
                INSERT INTO user_inventory (user_id,item_id)
                VALUES (:user_id,:item_id)
                                    """),gift_item)
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
                 return redirect(url_for("all_users"))
             else:
                flash('Invalid email or password')
            
              
        elif 'item_name' in request.form:  # This means the Create Item form was submitted
            duration_str = request.form['warranty_duration']
            warranty_days = int(duration_str) if duration_str.isdigit() else 0
            warranty_valid_until = date.today() + timedelta(days=warranty_days) if warranty_days else None
            create_item = {
                'item_name': request.form['item_name'],
                'item_image':request.form['item_image'],
                'original_price': request.form['original_price'],
                'current_price': request.form['original_price'],
                'item_size': request.form['item_size'],
                'item_color': request.form['item_color'],
                'in_stock': request.form['in_stock'],
                'warranty_duration':request.form['warranty_duration'],
                'warranty_valid_until':warranty_valid_until,
                'item_desc': request.form['item_desc'],
                'created_by': session['user_id']
            }
            db.session.execute(text("""
                INSERT INTO shop_item (item_name, item_image,original_price,current_price,item_size,item_color,in_stock,warranty_duration,warranty_valid_until, item_desc, created_by)
                VALUES (:item_name, :item_image, :original_price,:current_price, 
                        :item_size, :item_color, :in_stock, :warranty_duration,:item_desc,:warranty_valid_until, :created_by)
            """), create_item)
            db.session.commit()
    # Pagination for items in the shop
    # Because we don't want to change url, we are using a session variable
    if "item_page" not in session:
        session["item_page"] = 1
    if type(session["item_page"]) != int:
        session["item_page"] = 1
    item_page = session["item_page"]
    per_page = 10
    num_of_items=db.session.execute(text("SELECT count(item_id) as 'num_of_items' from shop_item")).mappings().fetchone()
    max_page = math.ceil(num_of_items['num_of_items']/per_page)
    if item_page > max_page:
        item_page = max_page
        session["item_page"] = item_page
    items = db.session.execute(text(f"SELECT * FROM shop_item LIMIT {per_page} OFFSET {(item_page-1) * per_page}")).all()
    # Page Memory to save current page status as we are on one page
    if "memory" not in session:
        session["memory"] = "None"
    inventory_stats = None
    if session['memory'] == "DUNGEON":
        session['html'] = 'battle.html'
        if 'user_id' in session:
            print('Stats?')
            inventory_stats = db.session.execute(text("""                      
                            SELECT 
                                i.equipped as 'equipped',
                                si.item_image as 'item_image',
                                s.*
                            FROM
                                user_inventory as i
                                    natural join
                                item_stats as s
                                    natural join
                                shop_item as si
                            WHERE 
                                i.item_id = s.item_id
                                and
                                i.item_id = si.item_id
                                and
                                i.user_id = :user_id
                            LIMIT 6
                            """), {"user_id": session['user_id']}).mappings().fetchall()
            print("HUH", inventory_stats)
    page_memory = session["memory"]
    #Pagination of users
    if "user_page" not in session:
        session["user_page"]=1
    if type(session['user_page'])!=int:
        session["user_page"]=1
    user_page=session["user_page"]
    num_of_users=db.session.execute(text("SELECT count(user_id) as 'num_of_users' from shop_user")).mappings().fetchone()
    per_page=3
    user_page=1
    max_pages=math.ceil(num_of_users['num_of_users']/per_page)
    if user_page>max_pages:
        user_page=max_pages
        session['user_page']=user_page
    users=db.session.execute(text(f"SELECT * FROM shop_user LIMIT {per_page} OFFSET {(user_page-1)*per_page}"))
    #chat logic
    to_user = None
    user_id = session['user_id']
    _chat = None
    if user_id:
        _chat = db.session.execute(text(f"SELECT * FROM chat WHERE user1={user_id} OR user2={user_id}")).mappings().fetchall()
    if 'to_user' not in session:
        session['to_user'] = None
    to_user=session['to_user']
    conversation=None
    if to_user != None and user_id != None:
        chatid = db.session.execute(text(
                    f"SELECT * FROM chat WHERE (user1={to_user}) AND (user2={user_id}) OR (user1={user_id}) AND (user2={to_user})")).first()
        if chatid == None:
            db.session.execute(text(f"INSERT INTO chat (user1, user2) VALUES ({user_id},{to_user})"))
            db.session.commit()
            chatid = db.session.execute(text(
                        f"SELECT * FROM chat WHERE (user1={to_user}) AND (user2={user_id}) OR (user1={user_id}) AND (user2={to_user})")).first()
        conversation = db.session.execute(
                    text(f"""
                        SELECT 
                            message.* , 
                            user1.username as 'username1' ,  
                            user2.username as 'username2' 
                        FROM 
                            message, shop_user as user1, shop_user as user2 
                        WHERE 
                            message.from_user = user1.user_id AND 
                            message.to_user = user2.user_id AND
                            forchat={chatid.chatid}
                        """)).mappings().fetchall()
    if request.form: 
        if "response" in request.form:
            db.session.execute(text(
                f"INSERT INTO message (forchat,conversation,comment_date,from_user,to_user) VALUES({chatid.chatid},'{request.form['response']}', NOW(), {user_id}, {to_user})"))
            db.session.commit()
            return redirect(url_for('all_users'))
    #reviews logic
    comments = None
    review_item_id = None
    if 'review_item_id' in session:
        review_item_id = session['review_item_id']
        comments=db.session.execute(text(f"SELECT * FROM review WHERE for_item={review_item_id}")).all()

    return render_template(html,
                           users=users,
                           admin_users=admin_users,
                           vendor_users=vendor_users,
                           customer_users=customer_users,
                           items=items,
                           creator=creator,
                           login=login,
                           cart_items=cart_items,
                           cart_total=cart_total,
                           user_orders=user_order,
                           order_items=order_items,
                           inventory_items=inventory_items,
                           battle=battle,
                           item_page=item_page,
                           max_page=max_page,
                           memory=page_memory,
                           page=user_page,
                           max_pages=max_pages,
                           _chat=_chat,
                           conversation=conversation,
                           comments = comments,
                           review_item_id=review_item_id,
                           inventory_stats=inventory_stats,
                           all_carts = all_carts
                           )
@app.route("/memory/<memory>", methods=["GET"])
def memory_update(memory):
    session["memory"] = memory
    print("Updating Memory to: ", memory)
    return redirect(url_for("all_users"))
@app.route("/item_page_increase", methods=["GET"])
def item_page_increase():
    if "item_page" not in session:
        session["item_page"] = 1
    session["item_page"] +=1
    print(session["item_page"])
    return redirect(url_for("all_users"))

@app.route("/item_page_decrease", methods=["GET"])
def item_page_decrease():
    if "item_page" not in session:
        session["item_page"] = 1
    session["item_page"] -=1
    if session["item_page"] == 0:
        session["item_page"] = 1
    print(session["item_page"])
    return redirect(url_for("all_users"))

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
 
@app.route('/item_from_cart', methods=['POST'])
def handle_remove_warranty():
    if 'user_id' in session:
        if request.form:
            if 'submit_remove' in request.form:
                user_id = session['user_id']
                try: 
                    print("user_id - ", user_id, "item_id - ",request.form["item_id"])
                    allCartThatMatches = db.session.execute(text("""
                                            SELECT * FROM shop_cart WHERE item_id = :item_id AND user_id = :user_id LIMIT 1
                                            """), 
                                    {
                                        "user_id": user_id, 
                                        "item_id": int(request.form["item_id"])
                                        }).all()
                    print(allCartThatMatches)
                    db.session.execute(text("""
                                DELETE FROM shop_cart WHERE item_id = :item_id AND user_id = :user_id LIMIT 1
                                            """), 
                                    {
                                        "user_id": user_id, 
                                        "item_id": int(request.form["item_id"])
                                        })
                    db.session.commit()
                    flash("Deleted")
                except Exception as e:
                    db.session.rollback()
                    flash(f'Error placeing order:{e}')
            elif 'submit_warranty' in request.form:
                flash("INSERT CODE FOR WARRANTY HERE")
                pass
    return redirect(url_for('all_users'))

        
        
@app.route('/to_order', methods=['GET','POST'])
def to_order():
    if request.method == 'GET':
        flash('Invalid access. Please use the cart form to submit an order.')
        return redirect(url_for('all_users'))
    if 'user_id' not in session:
        flash('Login Required')
        return redirect(url_for('memory'))
    
    user_id = session['user_id']

    try:
        #insert orders
        order_total = db.session.execute(text("SELECT sum(item.original_price) as 'cart_total' from shop_cart cross join shop_item as item where shop_cart.item_id = item.item_id and user_id = :user_id"), {"user_id": user_id}).first()
        db.session.execute(text("""
                            INSERT INTO shop_order (user_id, order_total, status)
                            VALUES (:user_id, :order_total, "PENDING")
                                """), 
                           {
                               "user_id": user_id,
                               "order_total": order_total.cart_total
                           })
        #pay for the order
        previousBalance = db.session.execute(text('select balance from shop_user where user_id = :user_id'), {"user_id": user_id}).mappings().fetchone()

        db.session.execute(text(f"""
                            UPDATE shop_user SET balance = {previousBalance.balance - order_total.cart_total} WHERE user_id = :user_id 
                                """), {"user_id": user_id})
        
        db.session.commit()
        
        result = db.session.execute(
            text("SELECT order_id FROM shop_order WHERE user_id = :user_id ORDER BY created_at DESC LIMIT 1"),
                {"user_id": user_id}
            ).first()
        latest_order_id = result.order_id if result else None
        cart = get_user_cart(user_id)
        for cartItem in cart:
            db.session.execute(text("""
                            insert into order_item (order_id, item_id, quantity, price, color, size, status)
                            VALUES (:order_id, :item_id, :quantity, :price, :item_color, :item_size, "Pending")
                            """), 
                            {
                                'order_id':latest_order_id,
                                'item_id': cartItem.item_id,
                                'quantity': cartItem.quantity,
                                'price': cartItem.original_price,
                                'item_color':cartItem.item_color,
                                'item_size':cartItem.item_size
                            })
        #then update cart!
        db.session.execute(text("""
                                delete from shop_cart
                                where user_id = :user_id ;
                                """), {'user_id':user_id})
        db.session.commit()
        flash('Order Placed!')
        return redirect(url_for('memory_update', memory="ORDERS"))
    except Exception as e:
        db.session.rollback()
        flash(f'Error placeing order:{e}')
        print(e)
        return redirect(url_for('memory_update', memory="None"))
    
def get_user_order(user_id, vendor_id):
    if user_id == None and vendor_id != None:
        try:
            y = db.session.execute(text("""
                select 
                    shop_item.item_name as "name",
                    order_item.quantity as "quantity",
                    shop_order.order_id as "order_id",
                    order_item.item_id as "item_id",
                    order_item.price as "price",
                    order_item.color as "color",
                    order_item.size as "size",
                    order_item.status as "status"
                from 
                    order_item 
                        cross join 
                    shop_item 
                        cross join
                    shop_order
                where 
                    shop_item.item_id = order_item.item_id
                        and 
                    order_item.order_id = shop_order.order_id
                        and
                    shop_item.created_by = :vendor_id
            """), {"vendor_id": vendor_id}).mappings().fetchall()
            order_ids = ''
            for i, item in enumerate(y):
                if i == len(y) - 1:
                    order_ids += str(item['order_id'])
                    break
                order_ids = order_ids + str(item['order_id']) + ', '
            x = db.session.execute(text(f"""
                    select *
                    from shop_order
                    where order_id in ({order_ids})""")).mappings().fetchall()
        except Exception as e:
            print(e)
        x = None
        y = None
    elif user_id == None and  vendor_id == None:
        y = db.session.execute(text("""
            select 
                shop_item.item_name as "name",
                order_item.quantity as "quantity",
                shop_order.order_id as "order_id",
                order_item.item_id as "item_id",
                order_item.price as "price",
                order_item.color as "color",
                order_item.size as "size",
                order_item.status as "status"
            from 
                order_item 
                    cross join 
                shop_item 
                    cross join
                shop_order
            where 
                shop_item.item_id = order_item.item_id
                    and 
                order_item.order_id = shop_order.order_id
        """), {"vendor_id": vendor_id}).mappings().fetchall()
        x = db.session.execute(text(f"""
                select *
                from shop_order
                """)).mappings().fetchall()

    else:
            
        x = db.session.execute(text("""
                select *
                from shop_order
                where shop_order.user_id = :user_id
            """),{'user_id':user_id}).mappings().fetchall()
        y = db.session.execute(text("""
            select 
                shop_item.item_name as "name",
                order_item.quantity as "quantity",
                shop_order.order_id as "order_id",
                order_item.item_id as "item_id",
                order_item.price as "price",
                order_item.color as "color",
                order_item.size as "size",
                order_item.status as "status"
            from 
                order_item 
                    cross join 
                shop_item 
                    cross join
                shop_order
            where 
                shop_item.item_id = order_item.item_id
                    and 
                order_item.order_id = shop_order.order_id
                    and
                shop_order.user_id = :user_id
        """), {"user_id": user_id}).mappings().fetchall()
    return [x,y]

@app.route('/update_order_status', methods=['POST'])
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
         'order_id':request.form['order_id'],
         'item_id':request.form['item_id']
     }
    print(order_data)
    try:
         
        db.session.execute(text("""
               update order_item set status = :status
                                where item_id = :item_id and order_id = :order_id
                                """),order_data)
        db.session.commit()   
        flash('Order Updated.')
        #check if order is complete
        order_items = db.session.execute(text("""
                        select * from order_item where order_id = :order_id
                                              """), order_data).mappings().fetchall()
        print(order_items)
        delivered = True
        for item in order_items:
            if item['status'] == "Pending":
                delivered = False
            if item['status'] == "Shipped":
                continue
        if delivered:
            print('order delivered')
            db.session.execute(text("update shop_order set status = 'Delivered' where order_id = :order_id"), order_data)
            db.session.commit()
        order = db.session.execute(text("""
                        select * from shop_order where order_id = :order_id
                                        """), order_data).mappings().first()
        if order.status == 'Delivered':
            print('add_inventory_order')
            return redirect(f'/add_inventory_order/{order_data['order_id']}')
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
#OLD CODE FOR REFERENCE
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

# Updating inventory based off a completed order   
@app.route('/add_inventory_order/<order_id>', methods=['GET'])
def add_inventory_order(order_id):
    print(order_id, "jiahoh") 
    try:
        print("TRY")
        order = db.session.execute(text(f"""
                    SELECT * FROM shop_order WHERE order_id = {order_id}
                                        """)).first()
        print(order, 'ha8g9eoa')
        user_id = order.user_id
        print('user+id', user_id)
        order_items = db.session.execute(text(f"""
                    SELECT * FROM order_item WHERE order_id = {order_id}
                                        """)).mappings().fetchall()
        print(order_items)
        for item in order_items:
            print('loop')
            print(item)
            inventory_data = {
                'user_id':user_id,
                'item_id': item['item_id'],
                'quantity': item['quantity']
            }
            print(inventory_data, 'ahuioeh;')
            #inventory = db.session.execute(text('select * from user_inventory where user_id = :user_id'), user_id).mappings().fetchone()
            db.session.execute(text("""
                                    insert into user_inventory(user_id, item_id, quantity)
                                    values(:user_id,:item_id, :quantity)
                                    on duplicate key update quantity = quantity + :quantity;
                                    """),inventory_data)
        db.session.commit()
        return redirect(url_for('all_users'))
    except Exception as e:
        flash(f'Error updating Inventory: {e}')

        return redirect(url_for('all_users'))
     
def get_user_inventory(user_id):
    return db.session.execute(text("""
        select 
            user_inventory.*,shop_item.*
        from
            user_inventory
                cross join 
            shop_item 
        where user_inventory.item_id = shop_item.item_id
        and user_inventory.user_id = :user_id
    """),{'user_id':user_id}).mappings().fetchall()


#this is for you to look at ronin!!!
@app.route('/equip_item/<int:item_id>', methods=['POST'])
def equip_item(item_id):
    user_id = session['user_id']
    try:
        countOfEquipped = db.session.execute(text('select count(equipped) as "Total" from user_inventory where equipped = true')).mappings().fetchone()
        print(countOfEquipped)
        if countOfEquipped.Total < 6:
            # Equip selected item
            db.session.execute(text("""
                update user_inventory
                set equipped = true
                where user_id = :user_id and item_id = :item_id
            """), {'user_id': user_id, 'item_id': item_id})
            db.session.commit()
            flash('Item equipped!')
        else:
            flash("Please unequip an item first!")
    except Exception as e:
        flash(f'Error equipping item: {e}')
    return redirect(url_for('all_users'))

@app.route('/coins_to_cash', methods=['POST'])
def coins_to_cash():
    if request.form:
        user_id = session['user_id']
        previousBalance = db.session.execute(text('select balance from shop_user where user_id = :user_id'), {"user_id": user_id}).mappings().fetchone()
        luck = int(request.form['luck'])
        coins = int(request.form['coins']) * luck
        db.session.execute(text(f"""
                    update shop_user set balance = { previousBalance.balance + coins } where user_id = {user_id}
                                """))
        db.session.commit()
        session['memory'] = 'None'
    return redirect(url_for('all_users'))

@app.route('/logout')
def logout():
    print(session.items())
    session.clear()
    print(session.items())
    flash('logged out.','info')
    return redirect(url_for('all_users'))

def get_user_cart(user_id):
    return db.session.execute(text("""
    select shop_item.*, count(shop_item.item_id) as "quantity"
    from 
        shop_cart
            join 
        shop_item 
            on shop_cart.item_id = shop_item.item_id
    where shop_cart.user_id = :user_id and is_ordered = False
    group by shop_item.item_id
    
"""), {'user_id': user_id}).mappings().fetchall()

@app.route("/chat", methods=['POST'])
def chat():
    user_id=session['user_id']
    admin_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Admin'")).mappings().fetchall()
    vendor_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Vendor'")).mappings().fetchall()
    customer_users = db.session.execute(text("SELECT * FROM shop_user WHERE user_type = 'Customer'")).mappings().fetchall()
    _chat = db.session.execute(text(f"SELECT * FROM chat WHERE user1={user_id} OR user2={user_id}")).mappings().fetchall()
    conversation=None
    chatid=db.session.execute(text(f"SELECT * FROM chat WHERE (user1={request.form["userid"]} AND user2={user_id}) OR (user1={user_id} AND user2={request.form["userid"]})")).first()
    if chatid==None:
        db.session.execute(text(f"INSERT INTO chat (user1, user2) VALUES ({request.form["userid"]},{user_id})"))
    db.session.commit()
    session['to_user'] = request.form['userid']    
    session['html'] = 'chat_01.html'
    if customer_users:
        for customer in customer_users:
            if customer['user_id'] == user_id:
                session['html'] = 'chat.html'
                break
    session['memory'] = "CHAT"
    return redirect(url_for("all_users"))
@app.route("/reviews/<item_id>", methods=['GET','POST'])
def reviewing(item_id):
    comments=db.session.execute(text(f"SELECT * FROM review WHERE for_item={item_id}")).all()
    if "review" in request.form:
        user_id=session['user_id']
        db.session.execute(text(f"INSERT INTO review (from_user,for_item,rating,review_date,statement) VALUES ({user_id},{item_id},{request.form["rating"]}, NOW(),'{request.form["review"]}')"))
        db.session.commit()
    session['review_item_id'] = item_id
    session['html'] = 'reviews.html'
    return redirect(url_for('all_users'))
@app.route('/update_item/<int:item_id>', methods=['POST'])
def update_item(item_id):
        duration_str = request.form['warranty_duration']
        warranty_days = int(duration_str) if duration_str.isdigit() else 0
        warranty_valid_until = date.today() + timedelta(days=warranty_days) if warranty_days else None
        update_item = {
                'item_name': request.form['item_name'],
                'item_image':request.form['item_image'],
                'original_price': request.form['original_price'],
                'current_price': request.form['original_price'],
                'item_size': request.form['item_size'],
                'item_color': request.form['item_color'],
                'in_stock': request.form['in_stock'],
                'warranty_duration':request.form['warranty_duration'],
                'warranty_valid_until':warranty_valid_until,
                'item_desc': request.form['item_desc'],
                'created_by': session['user_id'],
                'item_id':item_id
            }
        db.session.execute(text("""
                UPDATE shop_item
                SET item_name = :item_name,
                                item_image = :item_image,
                                original_price = :original_price,
                                current_price = :current_price,
                                item_size = :item_size,
                                item_color = :item_color,
                                in_stock = :in_stock,
                                warranty_duration = :warranty_duration,
                                warranty_valid_until = :warranty_valid_until,
                                item_desc = :item_desc,
                                created_by = :created_by
                                where item_id = :item_id 
            """), update_item)
        db.session.commit()
        flash('added to invertory!')
        return redirect(url_for('all_users'))

def get_all_carts():
    return db.session.execute(text("""
                                   SELECT
                                   u.user_id,
                                   u.username,
                                   i.item_id,
                                   i.item_name,
                                   i.original_price,
                                   c.is_ordered,
                                   COUNT(i.item_id) as quantity
                                FROM shop_cart c
                                JOIN shop_user u ON c.user_id = u.user_id
                                JOIN shop_item i ON c.item_id = i.item_id
                                WHERE c.is_ordered = FALSE
                                GROUP BY u.user_id, u.username, i.item_id, i.item_name, i.original_price, c.is_ordered
                                ORDER BY u.user_id
                                   """)).mappings().fetchall()
@app.route('/to_admin', methods=['POST'] )
def to_admin():
    user_id = {
        'user_id':request.form['user_id']
}
    db.session.execute(text("""
                            UPDATE shop_user
                            SET user_type = 'Admin'
                            WHERE user_id = :user_id
                            """),user_id)
    db.session.commit()
    flash('Made User into Admin!')
    return redirect(url_for('all_users'))
#update name
@app.route('/update_item_name', methods=['POST'])
def update_item_name():
    update ={
        'item_id':request.form['item_id'],
        'item_name':request.form['item_name']
    }
    db.session.execute(text("""
                            UPDATE shop_item
                            SET item_name = :item_name
                            WHERE item_id = :item_id
                            """),update)
    db.session.commit()
    flash('Item Name updated!')
    return redirect(url_for('all_users'))

#update original price
@app.route('/update_item_price', methods=['POST'])
def update_item_price():
    update ={
        'item_id':request.form['item_id'],
        'original_price':request.form['original_price']
    }
    db.session.execute(text("""
                            UPDATE shop_item
                            SET original_price = :original_price
                            WHERE item_id = :item_id
                            """),update)
    db.session.commit()
    flash('Item Price updated!')
    return redirect(url_for('all_users'))

    


#run#
if __name__ == '__main__':
    app.run(debug=True)