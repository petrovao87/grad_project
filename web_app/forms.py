from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})
    password = PasswordField('Пароль', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-info'})


class RegistrForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],    
                            render_kw={'class': 'form-control'})
    password1 = PasswordField('Пароль', validators=[DataRequired()],   
                            render_kw={'class': 'form-control'})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-info'})


class DownloadForm(FlaskForm):
    sample_name = StringField('Название образца', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})
    alloy_name = StringField('Название сплава', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})
    comment = StringField('Описание образца', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})

    upload = FileField('Загрузка изображения')
    submit_upload = SubmitField('Загрузить', render_kw={'class': 'btn btn-info'})

    image_scale = StringField('Увеличение при съемке', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})
    image_wb = StringField('Бинаризация', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})
    image_wb_min = IntegerField('Min', validators=[NumberRange(min=0, max=255)], 
                            render_kw={'class': 'form-control'})
    image_wb_max = IntegerField('Max', validators=[NumberRange(min=0, max=255)], 
                            render_kw={'class': 'form-control'})

    particle = StringField('Выбор частиц', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})
    particle_min = IntegerField('Выбор частиц Min', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})
    particle_max = IntegerField('Выбор частиц Max', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'}, default=1800000)
    submit = SubmitField('Проанализировать', render_kw={'class': 'btn btn-info'})

    average_size = StringField('Средний размер частиц, нм', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})
    deviation_size = StringField('Отклонение, нм', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})
    particles_number = StringField('Количество частиц', validators=[DataRequired()], 
                            render_kw={'class': 'form-control'})


class ProjectsForm(FlaskForm):
    use_all_experiments = SubmitField('Открыть все', render_kw={'class': 'btn btn-info'})
    use_experiment = SubmitField('Открыть', render_kw={'class': 'btn btn-info'})


