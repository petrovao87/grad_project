# PhaseCatcher

## This application allows you to analyze the particle size of the alloys from the image obtained with an electron microscope.

## Setting up

##### Clone the repo

```
$ git clone https://github.com/petrovao87/grad_project.git
$ cd grad_project
```

##### Add Environment Variables

Create a file called `config.env` that contains environment variables in the following syntax: `ENVIRONMENT_VARIABLE=value`.
You may also wrap values in double quotes like `ENVIRONMENT_VARIABLE="value with spaces"`.
For example, the mailing environment variables can be set as the following.
We recommend using Sendgrid for a mailing SMTP server, but anything else will work as well.

```
SECRET_KEY=Your_Secret_Key_Here
```

**Note: do not include the `config.env` file in any commits. This should remain private.**

##### Install the dependencies

```
$ pip install -r requirements.txt
```

##### Create the database

```
$ python create_db.py
```

## Running the app
```
$ export FLASK_APP=web_app && export FLASK_ENV=development && flask run
> set FLASK_APP=web_app && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
```