from flask import *
from config.config import *
from utils.user_utils import *

user_router  = Blueprint('user_model',__name__,static_folder='static', template_folder='views')
login_manager2.login_view = 'user_model.id_card_login'

@login_manager2.user_loader
def load_user(user_id):
    return LoadUserById(user_id)


@user_router.route('/')
def user_main_router():
    return render_template('prompt.html'),404

@user_router.route('/validate_id_card', methods=['POST'])
def validate_id_card_route():
    id_card = request.json['id_card']
    response = validate_id_card(id_card)
    return jsonify(response)


@user_router.route('/user/dashboard',methods=['POST','GET'])
@login_required
def user_dashboard():
    return render_template('form.html'),404



@user_router.route('/user', methods=['POST', 'GET'])
def id_card_login():
    try:
        if request.method == 'POST':
            id_card = request.form['id_card']
            user = get_user_id_card(id_card)
            if not user:
                error_message = 'Not a Member of the Panamenista Party.'
                return render_template('prompt.html', error_message=error_message)
            if not user.is_filled:
                error_message = 'Survey Form Already Filled.'
                return render_template('prompt.html', error_message=error_message)
            login_user(user)
            return redirect(url_for('user_model.user_dashboard'))
        return render_template('prompt.html')
    except Exception as e:
        error_message = 'Access denied'
        return render_template('prompt.html', error_message=error_message)


    
@user_router.route('/logout')
@login_required
def user_logout():
    success_message='User Successfully Logout'
    logout_user()
    return redirect(url_for('admin_model.admin_login',success_message=success_message))
    
    