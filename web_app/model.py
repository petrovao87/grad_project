from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
db.init_app(app)

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    image_scale = db.Column(db.Integer, nullable=False)
    image_wb = db.Column(db.Integer, nullable=False)
    image_cont = db.Column(db.Integer, nullable=False)
    experiment_time = db.Column(db.DateTime, nullable=False)

    sample_name = db.Column(db.String, nullable=False)
    alloy_name = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=True)

    average_size = db.Column(db.Integer, nullable=False)
    deviation_size = db.Column(db.Integer, nullable=False)
    shape_parameter = db.Column(db.Integer, nullable=False)
    particles_number = db.Column(db.Integer, nullable=False)

    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)

    def __repr__(self):
        return '<id: {}, name: {}>'.format(self.id, self.name)


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False, unique=True)
    uploaded = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    experiments = db.relationship(Experiment, backref='files')

    def __repr__(self):
        return '<file: {}, uploaded: {}>'.format(self.file_name, self.uploaded)


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