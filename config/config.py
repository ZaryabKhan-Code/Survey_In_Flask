from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from flask_bcrypt import Bcrypt
from flask_mail import *
import pdfkit
db = SQLAlchemy()
login_manager = LoginManager()
login_manager2 = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
Key = 'Survey_form'
def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zaryab@localhost/SurveyForm'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = Key
    app.config['MAIL_SERVER'] = 'mail2.anorco.com.pa'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'surveyadmin@anorco.com.pa'
    app.config['MAIL_PASSWORD'] = 'sXb2TXqENRRBCTjN'
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager2.init_app(app)
    bcrypt.init_app(app)

