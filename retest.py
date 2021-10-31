import pandas as pd
import os
import math
import random

def retestCreator(productName,ngrp,oser,members):

	path="/home/runner/JMA-Works/Downloads/"
	path=os.path.join(path,productName+'.xlsx')

	filename="/home/runner/JMA-Works/CSV/Main.csv"
	data=pd.read_csv(filename)
	data=data[data['Filed Against'] == productName]
	data=data[data['OS'] == oser]
	for i in ["Resolved","Retired","Rejected"]: 
		data=data[data['State'] != i]
	data = data[['ID', 'State', 'Severity','Title']].copy()
	data = data.where(pd.notnull(data), None)

	start_no=a=2
	end_no=(len(data.index)+1)
	
	if(ngrp=="three"):
		ngrp=3
	else:
		ngrp=2

	issue_grp=math.ceil((len(members))/ngrp)
	number_of_issues=end_no-start_no+1	

	span_grp=number_of_issues/issue_grp
	round_span_grp=math.ceil(span_grp)
	diff=issue_grp-(number_of_issues%issue_grp)

	main_list=list()
	if diff != issue_grp:
		for i in range(1,issue_grp+1):
			if i <= (issue_grp-diff):
				main_list.append(str(a)+" to "+str(a+round_span_grp-1))
				a=a+round_span_grp
			else:
				main_list.append(str(a)+" to "+str(a+round_span_grp-2))
				a=a+round_span_grp-1
	else:
		for i in range(1,issue_grp+1):
			main_list.append(str(a)+" to "+str(a+round_span_grp-1))
			a=a+round_span_grp

	random.shuffle(members)

	header=list()
	for i in range(ngrp):
		header.append("Group"+str(i+1))
	
	memberTable={"Issue List":main_list}

	count=0
	for i in range(ngrp):
		rowData=[]
		for j in range(len(main_list)):
			if count < len(members):
				rowData.append(members[count])
			else:
				rowData.append(None)
			count+=1
		memberTable[header[i]]=rowData

	#print(memberTable)
	df_member=pd.DataFrame(memberTable)
	#print(df_member)

	sheet_name = 'Retest Sheet'
	sheet_name2 = 'Assign Issue'

	writer= pd.ExcelWriter(path,engine='xlsxwriter')
	#data.to_excel(writer, sheet_name="Retest Sheet",index=False)
	data.to_excel(writer, sheet_name=sheet_name,index=False)
	df_member.to_excel(writer, sheet_name=sheet_name2,index=False)

	workbook  = writer.book
	worksheet = writer.sheets[sheet_name]
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

	cond_persists = workbook.add_format({
			'bg_color': '#FFC7CE',
			'font_color': '#9C0006',
			'border': 1,
			'text_wrap': True
			})

	cond_resolved = workbook.add_format({
			'bg_color': '#C6EFCE',
      'font_color': '#006100',
			'border': 1,
			'text_wrap': True,
			'valign': 'vcenter',
			'align' : 'center'
			})	

	cond_cbt = workbook.add_format({
			'bg_color': '#FFEB9C',
    	'font_color': '#9C6500',
			'border': 1,
			'text_wrap': True,
			'valign': 'vcenter',
			'align' : 'center'
			})	

	worksheet.set_column('A:A', 15)
	worksheet.set_column('B:B', 15)
	worksheet.set_column('C:C', 15)
	worksheet.set_column('D:D', 85)
	worksheet.set_row(0, 25)
	worksheet.set_column(4, end_no-1, 16)
	cond_persists.set_align('center')
	cond_persists.set_align('vcenter')

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

		##Conditional Formatting

	worksheet.data_validation(1, 4, end_no-1, ngrp+4-1, {'validate': 'list',
                                 'source': ['Persists', 'Resolved', 'Cannot be tested']})

	worksheet.conditional_format(1, 4, end_no-1, ngrp+4-1, {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':    '"Persists"',
                                    'format':   cond_persists})

	worksheet.conditional_format(1, 4, end_no-1, ngrp+4-1, {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':    '"Resolved"',
                                    'format':   cond_resolved})

	worksheet.conditional_format(1, 4, end_no-1, ngrp+4-1, {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':    '"Cannot be tested"',
                                    'format':   cond_cbt})

	c=0
	for i in range(4,ngrp+4):
		worksheet.write(0, i, header[c], header_format)
		c+=1
		
		##Assign Issue Formatting
	worksheet2.set_column('A:Z', 14)

	for col_num, value in enumerate(df_member.columns.values):
		worksheet2.write(0, col_num, value, header_format)

	r = 1
	c = 0

	for index, row in df_member.iterrows():
		worksheet2.write(r, c,row['Issue List'],header_format)
		for i in range(len(header)):
			worksheet2.write(r, c+i+1,row[header[i]],issue_format)
		r += 1

	writer.save()

