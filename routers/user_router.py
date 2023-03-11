from flask import *
from config.config import *
from utils.user_utils import *

user_router  = Blueprint('user_model',__name__,static_folder='static', template_folder='views')
login_manager2.login_view = 'user_model.user_dashboard'

@user_router.route('/')
def user_main_router():
    return render_template('prompt.html'),404

@user_router.route('/validate_id_card', methods=['POST'])
def validate_id_card_route():
    id_card = request.json['id_card']
    response = validate_id_card(id_card)
    return jsonify(response)


@user_router.route('/user',methods=['POST'])
def user_dashboard():
    return render_template('prompt.html'),404
@user_router.route('/h')
def user_main_form():
    return render_template('form.html'),404
