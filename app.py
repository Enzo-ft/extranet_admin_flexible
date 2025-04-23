from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
import shutil
import html_generator

app = Flask(__name__)
app.secret_key = 'change-this-secret-key'

UPLOAD_FOLDER = 'static/docs'
NETLIFY_FOLDER = '../site_etudiant'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'admin' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Identifiants incorrects")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        master = request.form['master']
        semestre = request.form['semestre']
        ue = request.form['ue']
        sous_dossier = request.form['sous_dossier']
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # 1. Enregistrement dans static/docs
            docs_path = os.path.join(app.config['UPLOAD_FOLDER'], master, semestre, ue, sous_dossier)
            os.makedirs(docs_path, exist_ok=True)
            file_path = os.path.join(docs_path, filename)
            file.save(file_path)

            # 2. Copie vers site_etudiant
            netlify_path = os.path.join(NETLIFY_FOLDER, master, semestre, ue, sous_dossier)
            os.makedirs(netlify_path, exist_ok=True)
            shutil.copy(file_path, os.path.join(netlify_path, filename))

            # 3. Mise à jour HTML étudiant
            html_generator.generate_html()

            return render_template('upload.html', success="Fichier uploadé avec succès ✅")
        else:
            return render_template('upload.html', success="❌ Seuls les fichiers PDF sont autorisés.")

    return render_template('upload.html')

@app.route('/docs')
def docs_etudiants():
    return render_template('docs_etudiants.html')

if __name__ == '__main__':
    os.makedirs('static/docs', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
