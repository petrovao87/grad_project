import requests
from web_app.model import db, FileDB
import os
import sys
from datetime import datetime
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

import os
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')




def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.Exception, ValueError):
        print('Сетевая ошибка')
        return False

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    print('UPLOAD!!!', file=sys.stdout)
    if request.method == 'POST':
        print('POST!!!', file=sys.stdout)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file, file=sys.stdout)
        print('FILE!!!', file=sys.stdout)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(UPLOAD_FOLDER, filename))
            uploaded = datetime.now()
            print(uploaded, file=sys.stdout)
            print(filename, file=sys.stdout)
            save_file(filename, uploaded)
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', file=sys.stdout)

            return redirect(url_for('uploaded_file', filename=filename))


def save_file(file_name, uploaded):
    print('!!!!!', file=sys.stderr)
    file_exists = FileDB.query.filter(FileDB.file_name == file_name).count()
    print(file_exists, file=sys.stderr)
    if not file_exists:
        file_2_db = FileDB(file_name=file_name, uploaded=uploaded)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@', file=sys.stderr)
        db.session.add(file_2_db)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@', file=sys.stderr)
        db.session.commit( )
    else:
        pass


def all_files(files):
    print('!!!!!', file=sys.stderr)
    files = FileDB.query.all()
    print(files, file=sys.stderr)
    if not files:
        return('В базе нет файлов')



if __name__ == '__main__':
    #html = get_html('https://www.python.org/blogs/')
    #if html:
        #with open('python.org.html', 'w', encoding='utf8') as f:
        #    f.write(html)
    #    news = get_python_news(html)
        print(news)


