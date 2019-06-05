from web_app.user.models import Files, User
from web_app.analyse.models import Experiment
from web_app.forms import ProjectsForm
from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user

blueprint = Blueprint('exist_project', __name__)


@blueprint.route('/projects', methods=['GET', 'POST'])
def projects():
    if current_user.is_authenticated:
        title = 'TEST'
        form = ProjectsForm()
        list_average_size = []
        list_deviation_size = []
        list_particles_number = []
        experiment_list = Experiment.query.order_by(Experiment.id).all()
        result_list = Experiment.query.order_by(Experiment.id).all()
        list_join = Experiment.query.join(Files, (Experiment.file_id == Files.id))\
            .join(User, (Files.user_id == User.id)).filter_by(id=current_user.id).all()
        if len(result_list) > 0:
            for result in result_list:
                list_average_size.append(result.average_size)
                list_deviation_size.append(result.deviation_size)
                list_particles_number.append(result.particles_number)
            average_dict = {'average_size': sum(list_average_size)/len(list_average_size),
                            'average_dv': sum(list_deviation_size)/len(list_deviation_size),
                            'average_pn': sum(list_particles_number)/len(list_particles_number)}
        else:
            average_dict = {'average_size': '~', 'average_dv': '~', 'average_pn': '~'}

        return render_template('projects.html', form=form, experiment_list=experiment_list, result_list=result_list,
                               title=title, average_dict=average_dict, list_join=list_join)
    else:
        return redirect(url_for('start.index'))