import pandas as pd
import os
from dateutil.parser import parse

def convert(x):
	try:
		dt=parse(x, fuzzy_with_tokens=True)
		return(dt[0].strftime('%d/%m/%Y'))
	except:
		return("")

def pivotCreator(productName,sheetLists,severityLists,oser,quarterwise):

	path="/home/runner/JMA-Works/Downloads/"
	path=os.path.join(path,productName+' pivot.xlsx')

	filename="/home/runner/JMA-Works/CSV/Main.csv"
	data=pd.read_csv(filename)
	#print(data)
	data['Created Date']=data['Created Date'].apply(convert)
	data['RTC Creation Date']=data['RTC Creation Date'].apply(convert)
	#data['RTC Creation Date']=data['RTC Creation Date'].apply(convert)

	data['Created Date'] = pd.to_datetime(data['Created Date'])
	data['RTC Creation Date'] = pd.to_datetime(data['RTC Creation Date'])

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

	print(data)
	if(quarterwise==1):
		start_date="2021-10-1"
		end_date="2021-10-14"
		mask = (data['Created Date'] >= start_date) & (data['Created Date'] <= end_date)
		data = data.loc[mask]

	print(data['Created Date'])
	data = data[['ID', 'State', 'Severity','Title']].copy()
	data = data.where(pd.notnull(data), None)

	sheet_name = 'Retest Sheet'

	writer= pd.ExcelWriter(path,engine='xlsxwriter')
	#data.to_excel(writer, sheet_name="Retest Sheet",index=False)
	data.to_excel(writer, sheet_name=sheet_name,index=False)

	workbook  = writer.book
	worksheet = writer.sheets[sheet_name]

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
	

	worksheet.set_column('A:A', 15)
	worksheet.set_column('B:B', 15)
	worksheet.set_column('C:C', 15)
	worksheet.set_column('D:D', 85)
	worksheet.set_row(0, 25)

	for col_num, value in enumerate(data.columns.values):
		worksheet.write(0, col_num, value, header_format)

	r = 1
	c = 0

	for index, row in data.iterrows():
		worksheet.write(r, c,row['ID'],issue_format)
		worksheet.write(r, c + 1,row['State'],issue_format)
		worksheet.write(r, c + 2,row['Severity'],issue_format)
		worksheet.write(r, c + 3,row['Title'],summary_format)
		r += 1
	writer.save()

