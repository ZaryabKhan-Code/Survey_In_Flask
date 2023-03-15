from config.config import *
class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True, index=True)
    password = db.Column(db.String(200))
    is_confirmed = db.Column(db.Boolean, default=False)
    
    def __init__(self, username, email, password,is_confirmed):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.is_confirmed = is_confirmed

class Form(db.Model):
    __tablename__='form'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_confirmed = db.Column(db.Boolean, default=False)    
    message = db.Column(db.String(200))
    
class Admin_confirmed(db.Model):
    __tablename__='admin_confirmed'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_confirmed_on = db.Column(db.Boolean, default=False)    
    


