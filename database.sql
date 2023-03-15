create database SurveyForm;
use SurveyForm;
create table form(
id int primary key auto_increment,
is_confirmed Boolean,
message varchar(200)
);
insert into form values(1,0,"Submission is off");
select * from form;
drop table form;
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
VALUES (1, 'John', 'Doe', '1-1234-12375', 'john.doe@example.com', '123 Main St', 'Anytown', 'Anyprovince', 'Anycountry', TRUE);

INSERT INTO user (id, first_name, last_name, id_card, current_email_address, address, city, province, country, is_filled)
VALUES (3, 'John', 'Doe', '1-1234-12345', 'john.doe@example.com', '123 Main St', 'Anytown', 'Anyprovince', 'Anycountry', FALSE);

INSERT INTO user (id, first_name, last_name, id_card, current_email_address, address, city, province, country, is_filled)
VALUES (4, 'John', 'Doe', '1-1234-12555', 'john.doe@example.com', '123 Main St', 'Anytown', 'Anyprovince', 'Anycountry', FALSE);

INSERT INTO user (id, first_name, last_name, id_card, current_email_address, address, city, province, country, is_filled)
VALUES (2, 'Jane', 'Doe', 'PE-1234-123456', 'jane.doe@example.com', '456 Oak St', 'Othertown', 'Otherprovince', 'Othercountry', FALSE);
select * from user;

truncate user;
CREATE TABLE other_information (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    gender VARCHAR(10),
    edad INT,
    date_of_birth Varchar(20),
    blood_type VARCHAR(10),
    blood_donor varchar(20),
    language VARCHAR(200),
    home_number VARCHAR(20),
    province VARCHAR(200),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
select * from other_information;
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
CREATE TABLE disability (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER,
    type VARCHAR(50),
    specific_disability VARCHAR(200),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
truncate user;
truncate other_information;
select * from disability;

CREATE TABLE University (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    student_center VARCHAR(200),
    bachelor_or_technician_1 VARCHAR(200),
    bachelor_or_technician_2 VARCHAR(200),
    mastery_1 VARCHAR(200),
    mastery_2 VARCHAR(200),
    doctrate VARCHAR(200),
    institute_or_technical_training_center VARCHAR(200),
    professional_education_and_training VARCHAR(200),
    vocational_training_or_additional_training VARCHAR(200),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

select * from university;
select * from DegreeProgram;
CREATE TABLE DegreeProgram (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    degree VARCHAR(200),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
select * from DegreeProgram;
CREATE TABLE vocationaltrainingcenters (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    vocationaltrainingcenters VARCHAR(200),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
truncate University;
select * from vocationaltrainingcenters;
CREATE TABLE TechnicalTraining (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    technicalTraining VARCHAR(200),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
select * from technicalTraining;
CREATE TABLE Diploma (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    diploma_image LONGBLOB,
    job_experience VARCHAR(200),
    identity_proof LONGBLOB,
    personal_photo LONGBLOB,
    filename_diploma_image varchar (100),
    filename_identity_proof varchar (100),
    filename_personal_photo varchar (100), 
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE institution (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    trainingcenter VARCHAR(200) NULL,
    othervocationaltraining VARCHAR(200) NULL,
    training VARCHAR(200) NULL,
    addtraining VARCHAR(200) NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
select * from institution;
select * from Diploma;
truncate Diploma;
truncate technicalTraining;
truncate university;
truncate vocationaltrainingcenters;
select * from technicalTraining;
truncate DegreeProgram;
select * from Diploma;
select * from vocationaltrainingcenters;
select * from disability;
select * from admin;
truncate admin;
