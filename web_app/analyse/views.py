from web_app.funcs import upload_file
from web_app.db import db
from web_app.user.models import Experiment
from web_app.user.models import Files
from web_app.forms import DownloadForm
from web_app.treatment import treatment
from flask import Blueprint, flash, request, redirect, url_for, send_from_directory, render_template, send_file, \
    jsonify, current_app
from flask_login import current_user
from datetime import datetime
from PIL import Image
from sqlalchemy import exc
import os
import logging

blueprint = Blueprint('analyse', __name__)


@blueprint.route('/mediafiles/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@blueprint.route('/kotik/kotik.jpg')
def kotik():
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], 'kotik.jpg')


@blueprint.route('/workdir/<filename>')
def workdir_uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"] + '/workdir', filename)


@blueprint.route('/workdir_final/final_<filename>')
def workdir_final_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], '/final_' + filename)


@blueprint.route('/analise', methods=['GET', 'POST'])
def analise():
    if current_user.is_authenticated:
        title = 'TEST'
        form = DownloadForm()
        if request.method == 'POST':
            filename = upload_file(current_user.id)
            contour_file(filename)
        else:
            filename = request.args.get('file')
        return render_template('analise.html', form=form, filename=filename, title=title)
    else:
        return redirect(url_for('start.index'))


@blueprint.route('/get-files/<filename>')
def crop_file(filename):
    area = (0, 0, 1600, 1115)
    basedir = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    filename_server = os.path.join(UPLOAD_FOLDER, filename)
    image_original = Image.open(filename_server)
    image_resize = image_original.resize((1600, 1200))
    image_cut = image_resize.crop(area)
    image_cut.save(os.path.join(UPLOAD_FOLDER, 'crop_' + filename), 'JPEG')
    return send_file(os.path.join(UPLOAD_FOLDER, 'crop_' + filename), attachment_filename='image.jpg')


@blueprint.route('/treat-files/<binar>/<particle>/<filename>/')
def contour_file(binar, particle, filename):
    basedir = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(basedir, '..', 'uploads')
    binar_min = int(binar.split('-')[0])
    binar_max = int(binar.split('-')[1])
    particle_min = int(particle.split('-')[0])
    particle_max = int(particle.split('-')[1])
    result = treatment(filename, binar_min, binar_max, particle_min, particle_max)
    return send_file(os.path.join(UPLOAD_FOLDER + result['final_image']), attachment_filename='image.jpg')


@blueprint.route('/gist-files/<binar>/<particle>/<filename>/')
def gist_file(binar, particle, filename):
    binar_min = int(binar.split('-')[0])
    binar_max = int(binar.split('-')[1])
    particle_min = int(particle.split('-')[0])
    particle_max = int(particle.split('-')[1])
    result = treatment(filename, binar_min, binar_max, particle_min, particle_max)
    return jsonify(result)


@blueprint.route('/save-files/<binar>/<particle>/<sample_name>/<alloy_name>/<comment>/<filename>/')
def save_file(binar, particle, sample_name, alloy_name, comment, filename):
    image_scale = 1000
    binar_min = int(binar.split('-')[0])
    binar_max = int(binar.split('-')[1])
    particle_min = int(particle.split('-')[0])
    particle_max = int(particle.split('-')[1])

    result = treatment(filename, binar_min, binar_max, particle_min, particle_max)
    average_size = result['medium_phase_size']
    deviation_size = result['sigma']
    particles_number = result['particle_count']
    dt = datetime.strptime(result['dt'], '%B%d%Y%H%M%S')

    file_id = Files.query.filter((Files.file_name == filename)).first().id
    new_experiment = Experiment(sample_name=sample_name, alloy_name=alloy_name, comment=comment,
                                image_scale=image_scale, binar_min=binar_min, binar_max=binar_max,
                                particle_min=particle_min, particle_max=particle_max,
                                experiment_time=dt, average_size=average_size,
                                deviation_size=deviation_size, particles_number=particles_number,
                                file_id=file_id)
    try:
        db.session.add(new_experiment)
        db.session.commit()
        flash('Запись добавлена')
        logging.info('The analysis results were added to the DB as %s', sample_name)
    except exc.IntegrityError:
        db.session.rollback()
        flash('Такая запись уже есть')
        print('INTEGRITY ERROR')
        logging.info('Sample name %s is already exist in DB', sample_name)
    except exc:
        print(exc, 'Ошибка')
        logging.info('Exception %s', exc)
    return redirect(url_for('start.start'))