import os

from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, send_file, send_from_directory, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from PIL import Image
from sqlalchemy import exc
from werkzeug.wrappers import Response

from web_app.funcs import  allowed_file, all_files, analise_file, get_html, save_file, upload_file
from web_app.forms import DownloadForm, LoginForm, ProjectsForm, RegistrForm
from web_app.model import db, Experiment,Files, User
from web_app.treatment import treatment


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Роуты для регистрации и авторизации пользователя
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

    # Роуты загрузки изображения
    @app.route('/mediafiles/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    @app.route('/kotik/kotik.jpg')
    def kotik():
        return send_from_directory(app.config["UPLOAD_FOLDER"], 'kotik.jpg')

    @app.route('/workdir/<filename>')
    def workdir_uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"] + '/workdir', filename)

    @app.route('/workdir_final/final_<filename>')
    def workdir_final_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], '/final_' + filename)

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

    # Роуты анализа изображения
    @app.route('/analise', methods=['GET', 'POST'])
    def analise():
        filename = None
        if current_user.is_authenticated:
            title = 'TEST'
            form = DownloadForm()
            print(current_user.id)
            if request.method == 'POST':
                print('POST')
                filename = upload_file(current_user.id)
                contour_file(filename)
            else:
                print('GET')
            return render_template('analise.html', form=form, filename=filename, title=title)
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
        return send_file(os.path.join(UPLOAD_FOLDER, 'crop_'+filename), 
                                    attachment_filename='image.jpg')

    @app.route('/treat-files/<binar>/<particle>/<filename>/')
    def contour_file(binar, particle, filename):
        """
        :param binanr: (int:min-int:max) /12-15/
        :param particle:
        :param filename:
        :return:
        """
        basedir = os.path.abspath(os.path.dirname(__file__))
        UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
        binar_min = int(binar.split('-')[0])
        binar_max = int(binar.split('-')[1])
        particle_min = int(particle.split('-')[0])
        particle_max = int(particle.split('-')[1])
        result = treatment(filename, binar_min, binar_max, particle_min, particle_max)
        return send_file(os.path.join(UPLOAD_FOLDER + result['final_image']), 
                                    attachment_filename='image.jpg')

    @app.route('/gist-files/<binar>/<particle>/<filename>/')
    def gist_file(binar, particle, filename):
        """
        :param binanr: (int:min-int:max) /12-15/
        :param particle:
        :param filename:
        :return:
        """
        binar_min = int(binar.split('-')[0])
        binar_max = int(binar.split('-')[1])
        particle_min = int(particle.split('-')[0])
        particle_max = int(particle.split('-')[1])
        result = treatment(filename, binar_min, binar_max, particle_min, particle_max)
        return jsonify(result)

   # Роуты сохранения и показа результатов анализа из базы
    @app.route('/save-files/<binar>/<particle>/<sample_name>/<alloy_name>/<comment>/<filename>/')
    def save_file(binar, particle, sample_name, alloy_name, comment, filename):
        """
        :param binanr: (int:min-int:max) /12-15/
        :param particle:
        :param filename:
        :return:
        """
        image_scale = 20000
        binar_min = int(binar.split('-')[0])
        binar_max = int(binar.split('-')[1])
        particle_min = int(particle.split('-')[0])
        particle_max = int(particle.split('-')[1])
        experiment_time = datetime.now()

        result = treatment(filename, binar_min, binar_max, particle_min, particle_max)
        average_size = result['medium_phase_size']
        deviation_size = result['sigma']
        particles_number = result['particle_count']

        file_id = Files.query.filter((Files.file_name == filename)).first().id
        print(file_id)
        new_experiment = Experiment(sample_name=sample_name, alloy_name=alloy_name, 
                                    comment=comment, image_scale=image_scale, 
                                    binar_min=binar_min, binar_max=binar_max,
                                    particle_min=particle_min, particle_max=particle_max,
                                    experiment_time=experiment_time, average_size=average_size,
                                    deviation_size=deviation_size, 
                                    particles_number=particles_number, file_id=file_id)
        try:
            db.session.add(new_experiment)
            db.session.commit()
            flash('Запись добавлена')
        except exc.IntegrityError:
            db.session.rollback()
            flash('Такая запись уже есть')
            print('INTEGRITY ERROR')
        except exc:
            print(exc, 'Ошибка')
        return redirect(url_for('start'))

    @app.route('/projects', methods=['GET', 'POST'])
    def projects():
        if current_user.is_authenticated:
            title = 'TEST'
            form = ProjectsForm()
            print(current_user.id)
            experiment_time = datetime.now()
            list_average_size = []
            list_deviation_size = []
            list_particles_number = []
            experiment_list = Experiment.query.order_by(Experiment.id).all()
            result_list = Experiment.query.order_by(Experiment.id).all()
            list_join = Experiment.query.join(Files, (Experiment.file_id == Files.id))\
                .join(User, (Files.user_id == User.id)).filter_by(id=current_user.id).all()
            for i in list_join:
                print(i.files.file_name, i.files.users.username, 'for')
            print(list_join, 'result')
            if len(result_list) > 0:
                for result in result_list:
                    list_average_size.append(result.average_size)
                    list_deviation_size.append(result.deviation_size)
                    list_particles_number.append(result.particles_number)
                average_dict = {'average_size': sum(list_average_size)/len(list_average_size),
                                'average_dv': sum(list_deviation_size)/len(list_deviation_size),
                                'average_pn': sum(list_particles_number)/len(list_particles_number)}
                print(average_dict, 'average')
            else:
                average_dict = {'average_size': '~', 'average_dv': '~', 'average_pn': '~'}

            return render_template('projects.html', form=form, experiment_list=experiment_list, 
                                result_list=result_list, title=title, average_dict=average_dict,
                                list_join=list_join)
        else:
            return redirect(url_for('index'))

    return app
