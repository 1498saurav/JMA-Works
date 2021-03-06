#import shutil
import os
import pandas as pd
import numpy as np

def processData():
	try:
		filename=""
		data_store = []
		for file in os.scandir("/home/runner/JMA-Works/CSV"):
			filename=file.path

		data=pd.read_csv(filename)
		data_pivot=pd.pivot_table(data,index="State",columns="Severity",values="Due Date",aggfunc=len,fill_value=0)
		data_pivot["Grand Total"] = data_pivot.sum(axis=1)
		data_pivot.loc["Grand Total"] = data_pivot.select_dtypes(np.number).sum()
		data_store.append(data_pivot)
		test=data_pivot
		filedAgainst = ["JioPages Mobility","Jio Saavn"]
		for i in filedAgainst:
			test=data[data['Filed Against'] == i]
			print(test)
		#	test=pd.pivot_table(test,index="State",columns="Severity",values="Due Date",aggfunc=len,fill_value=0)
		#	test["Grand Total"] = test.sum(axis=1)
		#	test.loc["Grand Total"] = test.select_dtypes(np.number).sum()
		#	data_store.append(test)

		#data_pivot=data_pivot.crosstab(Sever, rownames=['a'], colnames=['b', 'c'])
		#pd.crosstab(a, [b, c], rownames=['a'], colnames=['b', 'c'])
		print("Processing data_pivot!")
		print(data_pivot)

	except:
		print("Processing Failed!")

processData()