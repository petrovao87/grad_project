from flask import Flask, render_template
from web_app.funcs import get_html, allowed_file, upload_file, save_file, all_files
from web_app.model import db, Files, User, Experiment
from web_app.forms import LoginForm, RegistrForm, DownloadForm, ProjectsForm
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from datetime import datetime


def create_app():

    app = Flask(__name__)
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        title = 'TEST'
        files_list = Files.query.order_by(Files.uploaded.desc()).all()
        login_form = LoginForm()
        time = datetime.now()
        return render_template('index.html', files_list=files_list, form=login_form, time=time)

    @app.route('/mediafiles/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    @app.route('/start', methods=['GET', 'POST'])
    def start():
        if current_user.is_authenticated:
            form = DownloadForm()
            if request.method == 'POST':
                user_id = User.query.filter(User.username == current_user.username).first()
                filename = upload_file(current_user.id, form)
                return redirect(url_for('.analise', file=filename))

            
            print(current_user.id)
            
            return render_template('start_work.html', form=form, )
        else:
            return redirect(url_for('index'))

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        time = datetime.now()
        return render_template('login.html', page_title=title, form=login_form, time=time)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('start'))

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    @app.route('/registr')
    def registr():

        title = 'Регистрация'
        registr_form = RegistrForm()
        time = datetime.now()
        return render_template('registr.html', page_title=title, form=registr_form, time=time)

    @app.route('/process-registr', methods=['POST'])
    def process_registr():
        form = RegistrForm()

        if form.validate_on_submit():
            print(User.query.filter(User.username == form.username.data).count())
            if not User.query.filter(User.username == form.username.data).count():
                user = User.query.filter(User.username == form.username.data).first()
                if not form.password1.data == form.password2.data:
                    flash('Пароли не совпадают')
                    return redirect(url_for('registr'))

                new_user = User(username=form.username.data,)
                new_user.set_password(form.password1.data)

                db.session.add(new_user)
                db.session.commit()
                flash('Вы успешно зарегистрировались, авторизуйтесь!')
                return redirect(url_for('login'))

            flash('Такой пользователь уже существует')
            return redirect(url_for('login'))
        return redirect(url_for('login'))


    @app.route('/analise', methods=['GET', 'POST'])
    def analise():
        filename = None
        if current_user.is_authenticated:
            
            title = 'TEST'
            form = DownloadForm()
            print(current_user.id)
            if request.method == 'POST':
                user_id = User.query.filter(User.username == current_user.username).first()
                filename = upload_file(current_user.id, form)
            else:
                filename = request.args.get('file')
            return render_template('analise.html', form=form, filename=filename, title=title)
       
        else:
            return redirect(url_for('index'))

    


    # @app.route('/projects', methods=['GET', 'POST'])
    # def projects():
    #     if current_user.is_authenticated:
    #         title = 'TEST'
    #         form = ProjectsForm()
    #         print(current_user.id)
    #         experiment_time = datetime.now()
    #         #db_data = Experiment(name='exp', image_scale='1', image_wb='2', image_cont='3', experiment_time=experiment_time, file_id='1')
    #         files_list = Experiment.query.order_by(Experiment.experiment_time.desc()).all()
    #         #db.session.add(db_data)
    #         #db.session.commit()
    #         return render_template('projects.html', form=form, files_list=files_list, title=title)
    #     else:
    #         return redirect(url_for('index'))



    return app
