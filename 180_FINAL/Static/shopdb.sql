#create database shopdb;
use shopdb;

drop table if exists cart_object;
drop table if exists shop_wallet;
drop table if exists shop_cart;
drop table if exists shop_item;
drop table if exists shop_user;




#creating an admin first for sign in!

create table if not exists shop_user(
user_id int primary key auto_increment,
full_name varchar(55) not null,
email varchar(100) unique not null,
username varchar(100) not null,
password_hash varchar(100) not null,
user_type enum('Admin','Vendor','Customer') not null
);
alter table shop_user add user_image varchar(100) null;
create table shop_item(
item_id int primary key auto_increment,
item_name varchar(100) not null,
item_desc varchar(200) not null,
item_image varchar(200)  null,
item_warranty int null,
item_color varchar(33) null, 
item_size varchar(33) null,
in_stock int null,
created_by int not null,
original_price decimal(10,2) not null,
current_price decimal(10,2) not null
);
create table shop_cart(
cart_id int primary key auto_increment,
user_id int not null,
cart_total decimal(10,2) not null,
foreign key (user_id) references shop_user(user_id)
);
create table cart_object(
cart_id int not null,
item_id int not null,
foreign key (cart_id) references shop_cart(cart_id),
foreign key (item_id) references shop_item(item_id)
);

create table shop_wallet(
wallet_id int primary key auto_increment,
user_id int not null,
foreign key (user_id) references shop_user(user_id),
wallet_amount decimal(10,2) null
);
create table chat(
chatid int primary key auto_increment,
user1 int,
user2 int
);
create table message(
conversation varchar(255),
forchat int,
comment_date datetime,
comment_image varchar(100),
FOREIGN KEY (forchat) references chat(chatid)
);
