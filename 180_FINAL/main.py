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
@app.route('/')
def all_users():
    admin_users = db.session.execute( text("select * from shop_user where user_type = 'Admin'")
                                     ).mappings().fetchall()
    vendor_users = db.session.execute( text("select * from shop_user where user_type = 'Vendor'")
                                      ).mappings().fetchall()
    customer_users = db.session.execute( text("select * from shop_user where user_type = 'Customer'")
                                        ).mappings().fetchall()
    items = db.session.execute( text("select * from shop_item")
                                  ).mappings().fetchall()

    return render_template('test.html',
                            admin_users=admin_users,
                            vendor_users=vendor_users, 
                            customer_users=customer_users,
                            items=items)

#run#
if __name__ == '__main__':
    app.run(debug=True)