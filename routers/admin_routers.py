from flask import *
from config.config import *
from utils.admin_utils import *
import bcrypt

admin_router  = Blueprint('admin_model',__name__,static_folder='static', template_folder='views')
login_manager.login_view = 'admin_model.admin_login'


@login_manager.user_loader
def load_user(user_id):
    return LoadUserById(user_id)



@admin_router.route('/register', methods=['GET', 'POST'])
@login_required
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if not username or not email or not password or not confirm_password:
            error_message = 'Please fill out all fields.'
            return render_template('register.html', error_message=error_message)

        if password != confirm_password:
            error_message = 'Passwords do not match.'
            return render_template('register.html', error_message=error_message)

        existing_user = get_admin_username(username)
        if existing_user:
            error_message = 'That username is already taken.'
            return render_template('register.html', error_message=error_message)
        
        existing_email = get_admin_email(email)
        if existing_email:
            error_message = 'That email is already taken.'
            return render_template('register.html', error_message=error_message)

        new_user = Admin(username=username, email=email, password=password, is_confirmed=False)
        db.session.add(new_user)
        db.session.commit()
        send_verification_email(email,username)
        message = "Registration successful, activation link sent to email"
        return render_template('register.html', message=message)
    return render_template('register.html')


@admin_router.route('/admin', methods=['POST', 'GET'])
def admin_login():
    success_message = request.args.get('success_message')
    if current_user.is_authenticated:
        return redirect(url_for('admin_model.admin_dashboard'))
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = get_admin_email(email)
            if not user:
                error_message = 'Incorrect email or password.'
                return render_template('login.html', error_message=error_message, success_message=success_message)
            if not bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'):
                error_message = 'Incorrect email or password.'
                return render_template('login.html', error_message=error_message, success_message=success_message)
            login_user(user)
            return redirect(url_for('admin_model.admin_dashboard'))
        return render_template('login.html', success_message=success_message)
    except Exception as e:
        error_message = 'Login access denied'
        return render_template('login.html', error_message=error_message, success_message=success_message)

@admin_router.route('/check_email/<email>')
@login_required
def check_email(email):
    email_admin = get_admin_email(email)
    if email_admin:
        return jsonify({'error': 'Email already exists'})
    else:
        return jsonify({})
    
@admin_router.route('/check_username/<username>')
@login_required
def check_username(username):
    username_admin = get_admin_username(username)
    if username_admin:
        return jsonify({'error': 'Username already exists'})
    else:
        return jsonify({})

@admin_router.route('/activate')
def activate():
    if current_user.is_authenticated:
        return redirect(url_for('admin_model.admin_dashboard'))
    token = request.args.get('token')
    try:
        email = verify_activation_token(token)
        if email is not None:
            activate = get_admin_email(email)
            activate.is_confirmed = True
            db.session.commit()
            delete_token(token)
            flash('Your email has been verified. You can now log in.')
            return render_template('verification_result.html', success=True)
        else:
            return render_template('verification_result.html', success=False)       
    except Exception as e:
        return f'Error Creating Token Contact Support'




@admin_router.route('/dashboard/user')
@login_required
def admin_dashboard():
    try:
        return render_template('dashboard.html')
    except Exception as e:
        message = f'Error'
        return render_template('dashboard.html',message=message)
    
    
@admin_router.route('/logout')
@login_required
def admin_logout():
    success_message='User Successfully Logout'
    logout_user()
    return redirect(url_for('admin_model.admin_login',success_message=success_message))
    
    