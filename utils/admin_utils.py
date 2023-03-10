from models.admin_models import *
from config.config import *
from flask import *

def LoadUserById(user_id):
    return Admin.query.get(int(user_id))


def get_admin_email(email):
    return Admin.query.filter_by(email=email).first()


def get_admin_username(username):
    return Admin.query.filter_by(username=username).first()

import re
def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(regex, email))

def add_admin(username, email, password):
    admin = Admin(username=username,email=email,password=password)
    db.session.add(admin)
    db.session.commit()
    
import time,uuid,hashlib
import threading

token_hashes = {}

def generate_activation_token(email):
    payload = {'email': email, 'exp': time.time() + 300}
    token = str(uuid.uuid4().hex)[:10]
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    token_hashes[token_hash] = payload
    return token

def verify_activation_token(token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    payload = token_hashes.get(token_hash)
    if payload is not None and payload['exp'] > time.time():
        return payload['email']
    else:
        return None

def delete_token(token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    if token_hash in token_hashes:
        del token_hashes[token_hash]

def delete_expired_tokens():
    while True:
        time.sleep(60)
        now = time.time()
        expired_tokens = [token_hash for token_hash, payload in token_hashes.items() if payload['exp'] <= now]
        for token_hash in expired_tokens:
            del token_hashes[token_hash]
threading.Thread(target=delete_expired_tokens, daemon=True).start()

def send_verification_email(email,name):
    token = generate_activation_token(email)
    url = url_for('admin_model.activate', token=token, _external=True)
    msg = Message('Verify your email address', sender='surveyadmin@anorco.com.pa', recipients=[email])
    msg.html = render_template('verify_email.html', url=url,name=name)
    mail.send(msg)
    
    
def create_default_user():
    if Admin.query.filter_by(email='admin@example.com').first() is None:
        default_user = Admin(
            username='admin',
            email='admin@example.com',
            password=bcrypt.hashpw(b'password', bcrypt.gensalt()).decode('utf-8'),
            is_confirmed=True
        )
        db.session.add(default_user)
        db.session.commit()
