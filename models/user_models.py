from config.config import *
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_card = db.Column(db.String(200))
    current_email_address = db.Column(db.String(200))
    address = db.Column(db.String(200))
    city = db.Column(db.String(200))
    province = db.Column(db.String(200))
    country = db.Column(db.String(200))
    