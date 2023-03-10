from config.config import *
import bcrypt

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
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.is_confirmed = is_confirmed



