from flask import *
from config.config import *
from routers.admin_routers import admin_router
from utils.admin_utils import *

app = Flask(__name__, static_folder='static', template_folder='views')
init_app(app)
app.register_blueprint(admin_router)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_user()
    app.run(debug=True)