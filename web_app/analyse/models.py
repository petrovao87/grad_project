from web_app.db import db


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sample_name = db.Column(db.String, index=True, unique=True, nullable=False)
    alloy_name = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=True)

    image_scale = db.Column(db.Integer, nullable=False)
    binar_min = db.Column(db.Integer, nullable=False)
    binar_max = db.Column(db.Integer, nullable=False)
    particle_min = db.Column(db.Integer, nullable=False)
    particle_max = db.Column(db.Integer, nullable=False)
    experiment_time = db.Column(db.DateTime, nullable=False)

    average_size = db.Column(db.Integer, nullable=False)
    deviation_size = db.Column(db.Integer, nullable=False)
    particles_number = db.Column(db.Integer, nullable=False)

    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)

    def __repr__(self):
        return '<id: {}, name: {}>'.format(self.id, self.sample_name)