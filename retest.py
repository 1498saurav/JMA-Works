import pandas as pd
import os

def retestCreator(productName):

	path="/home/runner/JMA-Works/Downloads/"
	path=os.path.join(path,productName+'.xlsx')

	filename="/home/runner/JMA-Works/CSV/Main.csv"
	data=pd.read_csv(filename)
	data=data[data['Filed Against'] == productName]
	for i in ["Resolved","Retired","Rejected"]: 
		data=data[data['State'] != i]
	data = data[['ID', 'State', 'Severity','Title']].copy()
	data = data.where(pd.notnull(data), None)

	writer= pd.ExcelWriter(path,engine='xlsxwriter')
	data.to_excel(writer, sheet_name="Retest Sheet",index=False)

	writer.save()