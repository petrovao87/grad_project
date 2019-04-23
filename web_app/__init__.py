from flask import Flask, render_template
from web_app.funcs import get_html, allowed_file, upload_file, save_file, all_files, analise_file
from web_app.model import db, Files, User, Experiment
from web_app.forms import LoginForm, RegistrForm, DownloadForm, ProjectsForm
from web_app.treatment import treatment, treatment_analise
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, send_file, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from datetime import datetime
from PIL import Image
import os


def create_app():

    app = Flask(__name__)
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
                filename = upload_file(current_user.id)
                return redirect(url_for('analise', file=filename))
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
            #user = User.query.filter(User.username == form.username.data).first()
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
                print('POST')
                # user_id = User.query.filter(User.username == current_user.username).first()
                filename = upload_file(current_user.id)
                print(request.form['image_wb_min'], 'REQUEST FORM')
                contour_file(filename)
            else:
                print('GET')
                filename = request.args.get('file')
                if form.validate_on_submit():
                    crop_file(filename)
                    contour_file(filename)
                    session['filename'] = filename


            return render_template('analise.html', form=form, filename=filename, title=title)
            # user_id = User.query.filter(User.username == current_user.username).first()
            #analise_file(current_user.id, form)
        else:
            return redirect(url_for('index'))

    @app.route('/get-files/<filename>')
    def crop_file(filename):
        area = (0, 0, 1600, 1115)
        basedir = os.path.abspath(os.path.dirname(__file__))
        UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
        filename_server = os.path.join(UPLOAD_FOLDER, filename)
        image_original = Image.open(filename_server)
        image_resize = image_original.resize((1600, 1200))
        image_cut = image_resize.crop(area)
        image_cut.save(os.path.join(UPLOAD_FOLDER, 'crop_'+filename), 'JPEG')
        image_cut = 'crop_'+filename
        return send_file(os.path.join(UPLOAD_FOLDER, 'crop_'+filename), attachment_filename='image.jpg')

    @app.route('/treat-files/<filename>')
    def contour_file(filename):
        filename = session.get('filename')
        print(filename, 'CONTOUR FILE')
        basedir = os.path.abspath(os.path.dirname(__file__))
        print(basedir)
        UPLOAD_FOLDER = os.path.join(basedir, r'uploads\workdir\\')
        form = DownloadForm()
        treatment(filename, form.image_wb_min, form.image_wb_max, form.particle_min, form.particle_max)

        return send_file(os.path.join(UPLOAD_FOLDER, 'final_'+filename), attachment_filename='image.jpg')

    @app.route('/projects', methods=['GET', 'POST'])
    def projects():
        if current_user.is_authenticated:
            title = 'TEST'
            form = ProjectsForm()
            print(current_user.id)
            experiment_time = datetime.now()
            #db_exp = Experiment(name='exp3', image_scale='3', image_wb='3', image_cont='3',
            #                    experiment_time=experiment_time, file_id='1', sample_name='ccc',
            #                    alloy_name='ccc', comment='com3', average_size='3', deviation_size='3',
            #                    shape_parameter='3', particles_number='3'
            #                    )
            #db_files = Files(file_name='file3', uploaded=experiment_time, user_id='2')
            #db.session.add(db_exp)
            #db.session.add(db_files)
            #db.session.commit()
            list_average_size = []
            list_deviation_size = []
            list_shape_parameter = []
            list_particles_number = []
            experiment_list = Experiment.query.order_by(Experiment.id).all()
            result_list = Experiment.query.order_by(Experiment.id).all()
            list_join = Experiment.query.join(Files, (Experiment.file_id == Files.id))\
                .join(User, (Files.user_id == User.id)).filter_by(id=current_user.id).all()
            for i in list_join:
                print(i.files.file_name, i.files.users.username, 'for')
            print(list_join, 'result')
            for result in result_list:
                list_average_size.append(result.average_size)
                list_deviation_size.append(result.deviation_size)
                list_shape_parameter.append(result.shape_parameter)
                list_particles_number.append(result.particles_number)
            average_dict = {'average_size': sum(list_average_size)/len(list_average_size),
                           'average_dv': sum(list_deviation_size)/len(list_deviation_size),
                           'average_sp': sum(list_shape_parameter)/len(list_shape_parameter),
                            'average_pn': sum(list_particles_number)/len(list_particles_number)}
            print(average_dict, 'average')

            return render_template('projects.html', form=form, experiment_list=experiment_list, result_list=result_list,
                                   title=title, average_dict=average_dict, list_join=list_join)
        else:
            return redirect(url_for('index'))

    return app
