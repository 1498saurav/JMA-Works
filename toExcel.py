import pandas as pd
import os
def printExcel(data,path):
	try:
		print("started!")
		tables=data[0]
		titles=data[1]
		#titles.insert(0, "All")
		path=os.path.join(path,'Dashboard.xlsx')
		writer= pd.ExcelWriter(path,engine='xlsxwriter')

		#with pd.ExcelWriter('output.xlsx', mode='a') as writer:  
		#	for i in range(len(tables)):
		#		tables[i].to_excel(writer, sheet_name=titles[i])
		for i in range(len(tables)):
			tables[i].to_excel(writer, sheet_name=titles[i])

		writer.save()
		print("completed")
	except:
		print("converting to excel failed!")
