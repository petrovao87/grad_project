from flask import Flask, render_template
from web_app.funcs import get_html, allowed_file, upload_file, save_file, all_files
from web_app.model import db, FileDB
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template


def create_app():

    app = Flask(__name__)
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        title = 'TEST'
        upload_file()
        files_list = FileDB.query.order_by(FileDB.uploaded.desc()).all()




        return render_template('index.html', files_list=files_list)


    @app.route('/mediafiles/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


    return app

#if __name__ == '__main__':
#    app.run(debug=True)