import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import flash
import uuid

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/test')
def hello_world():
    return "hello world"


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        label = request.form['labelField']
        print(label)

        unique_filename = str(uuid.uuid4())
        print(unique_filename)
        text_file = open("Output.txt", 'a')
        text_file.write("\n" + unique_filename + " " + label)
        text_file.close()

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('Oups! Vous devez choisir une image!')
            return redirect(request.url)

        if label == '':
            flash("Oups! Vous devez faire la transcription écrit de l'image aussi!")
            return redirect(request.url)

        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                      unique_filename))
            flash("Merci pour nous aider! Vous pouvez téléverser d'autres photos :)")
            return redirect(url_for('upload_file'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
