create database SurveyForm;
use SurveyForm;
create table admin(
id int primary key auto_increment,
username varchar (200),
email varchar (200),
password varchar (200),
is_confirmed Boolean
);

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    id_card VARCHAR(200),
    current_email_address VARCHAR(200),
    address VARCHAR(200),
    city VARCHAR(200),
    province VARCHAR(200),
    country VARCHAR(200),
    is_filled BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id)
);
INSERT INTO user (id, first_name, last_name, id_card, current_email_address, address, city, province, country, is_filled)
VALUES (1, 'John', 'Doe', '1-1234-12345', 'john.doe@example.com', '123 Main St', 'Anytown', 'Anyprovince', 'Anycountry', TRUE);

INSERT INTO user (id, first_name, last_name, id_card, current_email_address, address, city, province, country, is_filled)
VALUES (2, 'Jane', 'Doe', 'PE-1234-123456', 'jane.doe@example.com', '456 Oak St', 'Othertown', 'Otherprovince', 'Othercountry', FALSE);


create table unregisteruser(
id int primary key auto_increment,
id_card varchar (200),
first_name varchar (200),
last_name varchar (200),
current_email_address varchar (200),
address varchar (200),
city varchar (200),
province varchar(200),
country varchar(200)
);

select * from admin;

truncate admin;