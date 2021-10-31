from flask import Flask, request, redirect, url_for,render_template,send_from_directory
from werkzeug.utils import secure_filename
import os

from filedAgainst import products,member
from retest import retestCreator
from newIssues import newIssueSheetCreator
from pivot import pivotCreator

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

@app.route('/fileUpload')
def fileUpload():
	return render_template("home.html")

@app.route('/retestCategory')
def retestCategoryDisplay():
	filedAgainstList = products()
	#print(filedAgainstList)
	return render_template("retestCategory.html",filedAgainstList=filedAgainstList,member=member)

@app.route('/rdownload', methods = ['GET', 'POST'])
def downloadRetest():
	productName= request.form['productType']
	ngrp = request.form['grpNum']
	oser=request.form['os']
	absentMembers=request.form.getlist('membersList')
	
	members=member.copy()
	for i in absentMembers:
		members.remove(i)
	#print(productName)
	retestCreator(productName,ngrp,oser,members)
	newIssueSheetCreator(productName)
	productName=productName+".xlsx"
	#productName=os.path.join("",".csv")
	return send_from_directory(app.config['DOWNLOAD_FOLDER'],productName,as_attachment=True)

@app.route('/dashboard')
def dashboard():
	filedAgainstList = products()
	return render_template("dashboard.html",filedAgainstList=filedAgainstList,sheetType=["Production","PreProd"],severityType=["Blocker","Critical","Major","Normal","Minor"])

@app.route('/analysis', methods = ['GET', 'POST'])
def downloadDashboard():
	productName= request.form['productType']
	sheetList = request.form.getlist('sheetList')
	severityList=request.form.getlist('severityList')
	oser=request.form['os']
	quarterwise=request.form['quarter']
	
	sheetLists=sheetList.copy()
	severityLists=severityList.copy()
	slist=["Blocker","Critical","Major","Normal","Minor"]
	if len(severityLists) == 0 or len(sheetLists) == 0:
		return redirect(url_for('dashboard'))
	severityLists = [i for i in severityLists + slist if i not in severityLists or i not in slist]

	#print(productName)
	pivotCreator(productName,sheetLists,severityLists,oser,quarterwise)
	productName=productName+" pivot.xlsx"
	#productName=os.path.join("",".csv")
	return send_from_directory(app.config['DOWNLOAD_FOLDER'],productName,as_attachment=True)

app.run(host='0.0.0.0', port=8080)