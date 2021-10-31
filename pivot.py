import pandas as pd
import numpy as np
import os
from dateutil.parser import parse
from quarter_processor import quarter
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

	#print(quarterwise)
	#print(data)
	if(int(quarterwise)==1):
		data=test(data)
		print("Quarter Wise Analysis!")
		#print(data)
		start_date= '2010-01-01'
		end_date= quarter()
		mask = (data['Created Date'] >= start_date) & (data['Created Date'] <= end_date)
		#print(mask)
		data = data.loc[mask]
		#print(data['Created Date'])

	#print(data['Created Date'])
	data = data[['ID', 'State', 'Severity','Title','Created Date']].copy()
	data = data.where(pd.notnull(data), None)

	data_pivot=pd.pivot_table(data,index="State",columns="Severity",values="Title",aggfunc=len,fill_value=0)
	data_pivot["Grand Total"] = data_pivot.sum(axis=1)
	data_pivot.loc["Grand Total"] = data_pivot.select_dtypes(np.number).sum()
	data_pivot = pd.DataFrame(data=data_pivot)
	data_pivot=data_pivot.dropna()
	
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

	pivot_issue_format = workbook.add_format({
			'text_wrap': True,
			'align' : 'center',
			'valign': 'vcenter'
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

	#worksheet1.set_column('A:Z', 14, issue_format)	

	#for col_num, value in enumerate(data_pivot.columns.values):
	#	worksheet1.write(0, col_num+1, value, header_format)

	df=data['State'].unique()
	df = pd.DataFrame(data=df)
	df=df.dropna()
	states=(df[0].to_list())
	states.append("Grand Total")
	#print(states)

	df1=data['Severity'].unique()
	df1 = pd.DataFrame(data=df1)
	df1=df1.dropna()
	#severity=(df1[0].to_list())
	#print(severity)

	#worksheet1.set_column(0,2+len(severity),18,header_format)
	#worksheet1.set_column(1,1+len(states),18,header_format)
	#worksheet1.set_column('A',18,header_format)
	#worksheet1.set_column('A',18,header_format)
	#worksheet1.set_column(0,(len(severity)+2),18, header_format)
	#df1 = pd.DataFrame(data=data_pivot)
	#df1=df1.dropna()
	#print(df1)

	#for i in range(len(states)+2):
	#	worksheet1.set_column(i,0,18,header_format)
	#for i in range(len(states)):
	#	worksheet1.write(i, 0, states[i], header_format)
	x=data_pivot.columns.values.tolist()
	states.insert(0,"State/Severity")
	#dp=[x] + [states]+ data_pivot.values.tolist()
	#y=data_pivot.values.tolist()
	#print(x,states,y)
	worksheet1.set_column('A:Z', 18, pivot_issue_format)
	for i in range(len(states)):
		worksheet1.write(i, 0, states[i], header_format)
		if i==0:
			for j in range(0,len(x)):
				#print(j)
				worksheet1.write(i, j+1, x[j], header_format)
		
	writer.save()

