import speech_recognition as sr 
r = sr.Recognizer()

import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from config import Config
from werkzeug.utils import secure_filename
from flask_wtf import Form, FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, validators, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = '/home/ismail/recognition_app/app/uploads'
ALLOWED_EXTENSIONS = set(['wav'])
DEBUG = os.getenv("FLASK_DEBUG", False)
#SECRET_KEY = "A0Zr98j/3yX R~ZJH!jmN]LWX/,?DT"

app = Flask(__name__)
#app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)
app.config['DEBUG'] = DEBUG
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.jinja_env.auto_reload = True


class UploadForm(FlaskForm):
    uploadfile = FileField(validators=[FileRequired(), FileAllowed(['wav'], 'Wavs only!')])
    submit = SubmitField('Upload Your shit!')

@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm(csrf_enabled=False)

    if form.validate_on_submit():
        f = form.uploadfile.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, filename))
        harvard = sr.AudioFile(os.path.join(UPLOAD_FOLDER, filename))
        with harvard as source:
            audio = r.record(source)
            text = r.recognize_google(audio, language='fr-FR')
        return render_template('index.html', form=form, test_ok = True, content_text = text)

    return render_template('index.html', form=form)