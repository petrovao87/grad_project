from web_app.funcs import upload_file
from web_app.user.models import Files
from web_app.forms import LoginForm, DownloadForm
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import current_user
from datetime import datetime


blueprint = Blueprint('start', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    files_list = Files.query.order_by(Files.uploaded.desc()).all()
    login_form = LoginForm()
    time = datetime.now()
    return render_template('index.html', files_list=files_list, form=login_form, time=time)


@blueprint.route('/start', methods=['GET', 'POST'])
def start():
    if current_user.is_authenticated:
        form = DownloadForm()
        if request.method == 'POST':
            filename = upload_file(current_user.id)
            return redirect(url_for('analyse.analise', file=filename))
        return render_template('start_work.html', form=form, )
    else:
        return redirect(url_for('start.index'))