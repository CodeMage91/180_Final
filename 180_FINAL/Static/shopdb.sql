#create database shopdb;
use shopdb;
drop table if exists message;
drop table if exists chat;
drop table if exists review;
drop table if exists user_inventory;
drop table if exists order_item;
drop table if exists shop_order;
drop table if exists shop_cart;
drop table if exists shop_item;
drop table if exists shop_user;

create table shop_user(
user_id int primary key auto_increment,
full_name varchar(55) not null,
email varchar(100) unique not null,
username varchar(100) not null,
password_hash varchar(100) not null,
user_type enum('Admin','Vendor','Customer') not null,
user_image varchar(200) null,
user_image_small varchar(200)  null
);

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
current_price decimal(10,2) null
);

create table shop_cart(
cart_id int primary key auto_increment,
user_id int not null,
item_id int not null,
is_ordered boolean default false,
foreign key (user_id) references shop_user(user_id),
foreign key (item_id) references shop_item(item_id)
);

create table shop_order(
order_id int primary key auto_increment,
user_id int not null,
order_total decimal(10,2) not null,
status enum('Pending','Shipped','Delivered') not null,
created_at timestamp default current_timestamp,
last_status_update timestamp default current_timestamp,
foreign key (user_id) references shop_user(user_id)
);

create table order_item(
order_items_id int primary key auto_increment,
order_id int not null,
item_id int not null,
quantity int null,
price decimal(10,2) not null,
color varchar(33) null,
size varchar(33) null,
status enum('Pending','Shipped','Delivered') not null,
foreign key (order_id) references shop_order(order_id),
foreign key (item_id) references shop_item(item_id)
);

create table user_inventory (
inventory_id int primary key auto_increment,
user_id int not null,
item_id int null,
quantity int default 1,
acquired_at timestamp default current_timestamp,
equipped boolean default false,
foreign key (user_id) references shop_user(user_id),
foreign key (item_id) references shop_item(item_id)
);
create table chat(
chatid int primary key auto_increment,
user1 int,
user2 int
);
create table message(
conversation varchar(255),
forchat int,
to_user int,
from_user int,
comment_date datetime,
comment_image varchar(100),
FOREIGN KEY (forchat) references chat(chatid)
);
create table review(
review_id int primary key auto_increment,
from_user int,
for_item int,
rating int,
review_image varchar(100),
review_date datetime,
statement varchar(255),
FOREIGN KEY (from_user) references shop_user(user_id),
FOREIGN KEY (for_item) references shop_item(item_id)
);