from config.config import *
class User(UserMixin,db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    id_card = db.Column(db.String(200))
    current_email_address = db.Column(db.String(200))
    address = db.Column(db.String(200))
    city = db.Column(db.String(200))
    province = db.Column(db.String(200))
    country = db.Column(db.String(200))
    is_filled = db.Column(db.Boolean,default=False)
    
    

class OtherInformation(db.Model):
    __tablename__ = 'other_information'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    gender = db.Column(db.String(10))
    edad = db.Column(db.Integer)
    date_of_birth = db.Column(db.String(20))
    blood_type = db.Column(db.String(10))
    blood_donor = db.Column(db.String(30))
    language = db.Column(db.String(200))
    home_number = db.Column(db.String(20))
    province = db.Column(db.String(200))
    
class Disability(db.Model):
    __tablename__ = 'disability'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(50))
    specific_disability = db.Column(db.String(200))
    
class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_center = db.Column(db.String(200))
    bachelor_or_technician_1 = db.Column(db.String(200))
    bachelor_or_technician_2 = db.Column(db.String(200),nullable=True)
    mastery_1 = db.Column(db.String(200))
    mastery_2 = db.Column(db.String(200),nullable=True)
    doctrate = db.Column(db.String(200),nullable=True)
    institute_or_technical_training_center = db.Column(db.String(200),nullable=True)
    professional_education_and_training = db.Column(db.String(200),nullable=True)
    vocational_training_or_additional_training = db.Column(db.String(200),nullable=True)

class DegreeProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    degree = db.Column(db.String(200),nullable=True)
    
class TechnicalTraining(db.Model):
    __tablename__='TechnicalTraining'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    technicalTraining= db.Column(db.String(200),nullable=True)
class Vocationaltrainingcenters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    Vocationaltrainingcenters = db.Column(db.String(200),nullable=True)

class Diploma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    diploma_image = db.Column(db.LargeBinary)
    job_experience = db.Column(db.String(200))
    identity_proof = db.Column(db.LargeBinary)
    personal_photo = db.Column(db.LargeBinary)
    