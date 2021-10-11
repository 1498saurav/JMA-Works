from flask import Flask, request, redirect, url_for,render_template,send_from_directory
from werkzeug.utils import secure_filename
import os

from processCSV import removeAllFiles,processData
from toExcel import printExcel
from filedAgainst import products

UPLOAD_FOLDER = '/home/runner/JMA-Works/CSV/'
DOWNLOAD_FOLDER = '/home/runner/JMA-Works/Downloads/'
ALLOWED_EXTENSIONS = {'csv'}
data=""

app = Flask('app')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

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

			f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename("Main.csv")))
			print("Uploaded Files!")
			return redirect(url_for('fileUpload'))
		else:
			print("Invalid File Type")
			return redirect(url_for('index'))

@app.route('/process')
def process():
	data=processData()
	data[1].insert(0, "All")
	#printExcel(data,app.config['DOWNLOAD_FOLDER'])
	#send_from_directory(app.config['DOWNLOAD_FOLDER'],"Dashboard.xlsx", as_attachment=True)
	#removeAllFiles()

	#print(data[0])
	return render_template("data.html",tables=[i.to_html() for i in data[0]], titles=[i for i in data[1]])

@app.route('/download/Dashboard.xlsx')
def downloadFile():
	print(app.config['DOWNLOAD_FOLDER'])
	printExcel(data,app.config['DOWNLOAD_FOLDER'])
	return send_from_directory(app.config['DOWNLOAD_FOLDER'],"Dashboard.xlsx", as_attachment=True)

@app.route('/fileUpload')
def fileUpload():
	return render_template("home.html")

@app.route('/retestCategory')
def retestCategoryDisplay():
	filedAgainstList = products()
	#print(filedAgainstList)
	return render_template("retestCategory.html",filedAgainstList=filedAgainstList)

app.run(host='0.0.0.0', port=8080) 