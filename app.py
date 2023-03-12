from flask import *
from config.config import *
from routers.admin_routers import admin_router
from routers.user_router import user_router
from utils.admin_utils import *
app = Flask(__name__, static_folder='static', template_folder='views')
import os
app.config['UPLOAD_FOLDER'] = os.path.join(user_router.static_folder, 'uploads')
init_app(app)
app.register_blueprint(admin_router)
app.register_blueprint(user_router)
from werkzeug.utils import secure_filename
import os
def save_file(file, folder):
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
        file.save(file_path)
        return filename
    else:
        return None
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_user()
    app.run(debug=True)