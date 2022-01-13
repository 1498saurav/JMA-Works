import pandas as pd
import os
import math
import random

def rtestCreator(productName,ngrp,oser,members):

	path="/home/runner/JMA-Works/Downloads/"
	path=os.path.join(path,productName+'.xlsx')

	filename="/home/runner/JMA-Works/CSV/Main.csv"
	data=pd.read_csv(filename)
	data=data[data['Filed Against'] == productName]
	data=data[data['OS'] == oser]
	for i in ["Resolved","Retired","Rejected","Defer"]: 
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
	df_member=pd.DataFrame(memberTable)
	data_newIssues = pd.DataFrame(columns=['Sr No.','Title','Path','Description','Device Tested On','Android Version','Domain ID','BOC Validations','Severity'])

	with pd.ExcelWriter(path) as writer:  
		data.to_excel(writer, sheet_name="Retest Sheet",index=False)
		df_member.to_excel(writer,sheet_name="Assign Issue",index=False)
		data_newIssues.to_excel(writer,sheet_name="New Issues",index=False)

