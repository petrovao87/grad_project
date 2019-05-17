from flask import Flask
from flask_login import LoginManager
from web_app.funcs import get_html, allowed_file, upload_file, save_file, all_files, analyse_file
from web_app.db import db
from web_app.user.models import Files, User
from web_app.analyse.models import Experiment
from web_app.forms import LoginForm, RegistrForm, DownloadForm, ProjectsForm
from web_app.treatment import treatment
from web_app.start.views import blueprint as start_blueprint
from web_app.user.views import blueprint as user_blueprint
from web_app.analyse.views import blueprint as analyse_blueprint
from web_app.exist_project.views import blueprint as exist_project_blueprint
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='func_log.log'
                    )


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(start_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(analyse_blueprint)
    app.register_blueprint(exist_project_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
