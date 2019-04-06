from flask_sqlalchemy import SQLAlchemy
from flask import Flask



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
db.init_app(app)

class FileDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False, unique=True)
    user = db.Column(db.String, nullable=True)
    uploaded = db.Column(db.DateTime, nullable=False)
    #text = db.Column(db.Text, nullable=True)


    def __repr__(self):
        return '<file: {}, uploaded: {}>'.format(self.file_name, self.uploaded)