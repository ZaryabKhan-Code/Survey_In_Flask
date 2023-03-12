from models.user_models import *
from config.config import *
from flask import *
import re

def LoadUserById(user_id):
    return User.query.get(int(user_id))

def get_user_id_card(id):
    return User.query.filter_by(id_card=id).first()

def get_user_by_email(email):
    return User.query.filter_by(current_email_address=email).first()

def get_user_other_user_information(id):
    return OtherInformation.query.filter_by(user_id=id).first()

def get_user_disability(id):
    return Disability.query.filter_by(user_id=id).first()

def validate_id_card(id_card):
    regular_pattern = re.compile("^\d{1}-\d{4}-\d{5}$")
    panameno_pattern = re.compile("^PE-\d{4}-\d{6}$")
    extranjero_pattern = re.compile("^E-\d{4}-\d{5}$")
    naturalizado_pattern = re.compile("^N-\d{4}-\d{5}$")
    vigencia_pattern = re.compile("^\d{1}AV-\d{4}-\d{5}$")
    indigena_pattern = re.compile("^\d{1}PI-\d{4}-\d{5}$")
    if regular_pattern.match(id_card):
        response = {"status": "success", "message": "Valid regular ID card"}
    elif panameno_pattern.match(id_card):
        response = {"status": "success", "message": "Valid Panamanian born abroad ID card"}
    elif extranjero_pattern.match(id_card):
        response = {"status": "success", "message": "Valid foreigner ID card"}
    elif naturalizado_pattern.match(id_card):
        response = {"status": "success", "message": "Valid naturalized ID card"}
    elif vigencia_pattern.match(id_card):
        response = {"status": "success", "message": "Valid pre-vigency ID card"}
    elif indigena_pattern.match(id_card):
        response = {"status": "success", "message": "Valid indigenous population ID card"}
    else:
        response = {"status": "error", "message": "Invalid ID card"}
    return response