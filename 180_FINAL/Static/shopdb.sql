create database shopdb;
use shopdb;

#creating an admin first for sign in!

create table shop_user(
user_id int primary key auto_increment,
full_name varchar(55) not null,
email varchar(100) unique not null,
username varchar(100) not null,
password_hash varchar(100) not null,
user_type enum('Admin','Vendor','Customer') not null
);
alter table shop_user add user_image varchar(100) null;
update shop_user 
set user_image = 'isaac.png' where user_id = 2;

select * from shop_user;
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
drop table shop_item;
#user table created. Now time to add an admin
insert into shop_user(full_name, email, username, password_hash, user_type)
values('Devin Ayala', 'devin15Takidan@email.com', 'Tahdah25', '1234', 'Admin');

update shop_user
set user_image = 'devin.png';

update shop_wallet
set wallet_amount = 42.13;


alter table shop_item modify original_price decimal(10,2) not null;
select item_id, item_name, original_price from shop_item;

select * from shop_cart;
alter table shop_cart add total_items int null;


select * from shop_user where user_id = 1;
select * from shop_item;

create table shop_cart(
cart_id int primary key auto_increment,
user_id int not null,
cart_total decimal(10,2) not null,
foreign key (user_id) references shop_user(user_id)
);
select * from shop_cart;
insert into shop_cart(user_id,cart_total)
values(1,0.00);

select * from shop_user;

create table shop_wallet(
wallet_id int primary key auto_increment,
user_id int not null,
foreign key (user_id) references shop_user(user_id),
wallet_amount decimal(10,2) null
);
select * from shop_wallet;
select * from shop_item;
insert into shop_wallet(user_id, wallet_amount)
values(1,420.00);

create table cart_object(
cart_id int not null,
item_id int not null,
foreign key (cart_id) references shop_cart(cart_id),
foreign key (item_id) references shop_item(item_id)
);
select * from cart_object;
select * from shop_item;
insert into cart_object(cart_id, item_id)
values(1,1);

