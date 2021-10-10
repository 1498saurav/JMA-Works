from flask import Flask, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
import os

from processCSV import removeAllFiles,processData

UPLOAD_FOLDER = '/home/runner/JMA-Works/CSV/'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask('app')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
   return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/test', methods = ['GET', 'POST'])
def test():
	if request.method == 'POST':

		if 'data' not in request.files:
			print('No file part')
			return redirect(url_for('index'))

		f = request.files['data']

		if f.filename == '':
			print('No selected file')
			return redirect(url_for('index'))

#f.save(secure_filename(f.filename))
		if f and allowed_file(f.filename):	

			f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
			print("Uploaded Files!")
			return redirect(url_for('process'))
		else:
			print("Invalid File Type")
			return redirect(url_for('index'))

@app.route('/process')
def process():
	data=processData()
	removeAllFiles()
	return(data.to_html())		

app.run(host='0.0.0.0', port=8080)