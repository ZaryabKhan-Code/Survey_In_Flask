create database SurveyForm;
use SurveyForm;
create table admin(
id int primary key auto_increment,
username varchar (200),
email varchar (200),
password varchar (200),
is_confirmed Boolean
);

create table user(
id int primary key auto_increment,
id_card varchar (200),
current_email_address varchar (200),
address varchar (200),
city varchar (200),
province varchar(200),
country varchar(200)
);
create table unregisteruser(
id int primary key auto_increment,
id_card varchar (200),
current_email_address varchar (200),
address varchar (200),
city varchar (200),
province varchar(200),
country varchar(200)
);
select * from admin;

truncate admin;