from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from web_app.db import db
from web_app.analyse.models import Experiment


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False, unique=True)
    uploaded = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    experiments = db.relationship(Experiment, backref='files')

    def __repr__(self):
        return '<id : {}, file: {}, uploaded: {}>'.format(self.id, self.file_name, self.uploaded)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(128))

    db_files = db.relationship(Files, backref='users')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)