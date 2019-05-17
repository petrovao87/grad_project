from web_app.db import db
from web_app.user.models import User
from web_app.forms import LoginForm, RegistrForm
from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user
from datetime import datetime

blueprint = Blueprint('user', __name__)


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('start.index'))
    title = 'Авторизация'
    login_form = LoginForm()
    time = datetime.now()
    return render_template('login.html', page_title=title, form=login_form, time=time)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы вошли на сайт')
            return redirect(url_for('start.start'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('start.index'))


@blueprint.route('/registr')
def registr():
    title = 'Регистрация'
    registr_form = RegistrForm()
    time = datetime.now()
    return render_template('registr.html', page_title=title, form=registr_form, time=time)


@blueprint.route('/process-registr', methods=['POST'])
def process_registr():
    form = RegistrForm()
    if form.validate_on_submit():
        if not User.query.filter(User.username == form.username.data).count():
            if not form.password1.data == form.password2.data:
                flash('Пароли не совпадают')
                return redirect(url_for('user.registr'))
            new_user = User(username=form.username.data,)
            new_user.set_password(form.password1.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались, авторизуйтесь!')
            return redirect(url_for('user.login'))
        flash('Такой пользователь уже существует')
        return redirect(url_for('user.login'))
    return redirect(url_for('user.login'))