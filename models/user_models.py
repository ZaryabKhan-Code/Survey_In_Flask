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
