#import shutil
import os
import pandas as pd
import numpy as np

def processData():
	filedAgainst=""
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
		
		df=data['Filed Against'].unique()
		df = pd.DataFrame(data=df)
		df=df.dropna()
		#df[0].to_string(index=False)
		filedAgainst=(df[0].to_list())
		print(filedAgainst)
		
		test=data_pivot
		for i in ["JioPages Mobility","Jio Saavn"]:
			test=data[data['Filed Against'] == i]
			test=pd.pivot_table(test,index="State",columns="Severity",values="Due Date",aggfunc=len,fill_value=0)
			test["Grand Total"] = test.sum(axis=1)
			test.loc["Grand Total"] = test.select_dtypes(np.number).sum()
			data_store.append(test)

		#data_pivot=data_pivot.crosstab(Sever, rownames=['a'], colnames=['b', 'c'])
		#pd.crosstab(a, [b, c], rownames=['a'], colnames=['b', 'c'])
		print("Processing data_pivot!")
		print(data_pivot)
		return test
		
	except:
		print("Processing Failed!")

def removeAllFiles():
	#shutil.rmtree("/home/runner/JMA-Works/CSV")
	print("Removing Files!")
	for file in os.scandir("/home/runner/JMA-Works/CSV"):
		os.remove(file.path)
		