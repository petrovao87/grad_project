# PhaseCatcher

## This application allows you to analyze the particle size of the alloys from the image obtained with an electron microscope.

## Setting up

##### Clone the repo

```
$ git clone https://github.com/petrovao87/grad_project.git
$ cd grad_project
```

##### Install the dependencies

```
$ pip install -r requirements.txt
```

##### Create the database

```
$ python create_db.py
```

## Running the app and Add Environment Variables
**Note: Write down your secret key in first environment variable `SECRET_KEY` like shows in example**
```
$ export SECRET_KEY=Your_Secret_Key && export FLASK_APP=web_app && export FLASK_ENV=development && flask run
> set SECRET_KEY=Your_Secret_Key && set FLASK_APP=web_app && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
```