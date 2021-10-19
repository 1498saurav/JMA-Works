import pandas as pd
import numpy as np
import os
from dateutil.parser import parse

#data=""
#filename="/home/runner/JMA-Works/CSV/Main.csv"
#data=pd.read_csv(filename)

def convert(x):
	try:
		dt=parse(x, fuzzy_with_tokens=True)
		return (dt[0].strftime('%Y-%m-%d'))
	except:
		return("")

def test(data):
	data["Created Date"]=data["Created Date"].apply(convert)
	data['Created Date'] = pd.to_datetime(data['Created Date'])
	return data

def pivotCreator(productName,sheetLists,severityLists,oser,quarterwise):

	path="/home/runner/JMA-Works/Downloads/"
	path=os.path.join(path,productName+' pivot.xlsx')

	filename="/home/runner/JMA-Works/CSV/Main.csv"
	data=pd.read_csv(filename)
	#print(data)
	#data['Created Date']=data['Created Date'].apply(convert)
	#data['RTC Creation Date']=data['RTC Creation Date'].apply(convert)
	#data['RTC Creation Date']=data['RTC Creation Date'].apply(convert)

	#data=test(data)

	#data['Created Date'] = pd.to_datetime(data['Created Date'])
	#data['RTC Creation Date'] = pd.to_datetime(data['RTC Creation Date'])

	data=data[data['Filed Against'] == productName]
	data=data[data['OS'] == oser]
	for i in ["Resolved","Retired","Rejected"]: 
		data=data[data['State'] != i]
		
	if len(sheetLists)!= 2:
		if sheetLists[0]=="Production":
			data=data[data['Environment'] == "Production"]
		else:
			data=data[data['Environment'] != "Production"]

	for i in severityLists: 
		data=data[data['Severity'] != i]		

	print(quarterwise)
	#print(data)
	if(int(quarterwise)==1):
		data=test(data)
		print("Checking")
		print(data)
		start_date= '2021-10-01'
		end_date= '2021-10-19'
		mask = (data['Created Date'] >= start_date) & (data['Created Date'] <= end_date)
		#print(mask)
		data = data.loc[mask]
		print(data['Created Date'])

	#print(data['Created Date'])
	data = data[['ID', 'State', 'Severity','Title']].copy()
	data = data.where(pd.notnull(data), None)

	data_pivot=pd.pivot_table(data,index="State",columns="Severity",values="Title",aggfunc=len,fill_value=0)
	data_pivot["Grand Total"] = data_pivot.sum(axis=1)
	data_pivot.loc["Grand Total"] = data_pivot.select_dtypes(np.number).sum()

	sheet_name1 = 'Summary'
	sheet_name2 = 'Issues Sheet'

	writer= pd.ExcelWriter(path,engine='xlsxwriter')
	#data.to_excel(writer, sheet_name="Retest Sheet",index=False)
	data_pivot.to_excel(writer, sheet_name=sheet_name1)
	data.to_excel(writer, sheet_name=sheet_name2,index=False)
	

	workbook  = writer.book
	worksheet1 = writer.sheets[sheet_name1]
	worksheet2 = writer.sheets[sheet_name2]

	header_format = workbook.add_format({
			'border': 1,
			'bg_color': '#FFFF00',
			'bold': True,
			'text_wrap': True,
			'align': 'center',
			'valign': 'vcenter',
			})

	issue_format = workbook.add_format({
			'border': 1,
			'text_wrap': True,
			'align' : 'center',
			'valign': 'vcenter'
			})

	summary_format = workbook.add_format({
			'border': 1,
			'text_wrap': True,
			'valign': 'vcenter',
			'align' : 'vjustify'
			})
	
	worksheet2.set_column('A:A', 15)
	worksheet2.set_column('B:B', 15)
	worksheet2.set_column('C:C', 15)
	worksheet2.set_column('D:D', 85)
	worksheet2.set_row(0, 25)

	for col_num, value in enumerate(data.columns.values):
		worksheet2.write(0, col_num, value, header_format)

	r = 1
	c = 0

	for index, row in data.iterrows():
		worksheet2.write(r, c,row['ID'],issue_format)
		worksheet2.write(r, c + 1,row['State'],issue_format)
		worksheet2.write(r, c + 2,row['Severity'],issue_format)
		worksheet2.write(r, c + 3,row['Title'],summary_format)
		r += 1



	writer.save()

