create database SurveyForm;
use SurveyForm;
create table admin(
id int primary key auto_increment,
username varchar (200),
email varchar (200),
password varchar (200),
is_confirmed Boolean
);
select * from admin;