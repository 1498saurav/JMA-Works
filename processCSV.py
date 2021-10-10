#import shutil
import os
import pandas as pd
import numpy as np
filedAgainst=""
##filename=""
#for file in os.scandir("/home/runner/JMA-Works/CSV"):
#	filename=file.path
#data=pd.read_csv(filename)

def processData():
	try:
		filename=""
		data_store = []
		for file in os.scandir("/home/runner/JMA-Works/CSV"):
		 filename=file.path

		#Main Data to be not modified at any cost!
		data=pd.read_csv(filename)
		
		#Total Pivot Table of Media Apps
		data_pivot=pd.pivot_table(data,index="State",columns="Severity",values="Due Date",aggfunc=len,fill_value=0)
		data_pivot["Grand Total"] = data_pivot.sum(axis=1)
		data_pivot.loc["Grand Total"] = data_pivot.select_dtypes(np.number).sum()
		data_store.append(data_pivot)
		
		#Filed Against is Available Here!
		df=data['Filed Against'].unique()
		df = pd.DataFrame(data=df)
		df=df.dropna()
		#df[0].to_string(index=False)
		filedAgainst=(df[0].to_list())
		#print(filedAgainst)

		#filedAgainst=filedAgainst()

		test=""
		for i in filedAgainst:
			test=data[data['Filed Against'] == i]
			#print(test)
			test=pd.pivot_table(test,index="State",columns="Severity",values="Due Date",aggfunc=len,fill_value=0)
			test["Grand Total"] = test.sum(axis=1)
			test.loc["Grand Total"] = test.select_dtypes(np.number).sum()
			#print(test)
			data_store.append(test)

		#data_pivot=data_pivot.crosstab(Sever, rownames=['a'], colnames=['b', 'c'])
		#pd.crosstab(a, [b, c], rownames=['a'], colnames=['b', 'c'])
		print("Processing data_pivot!")
		#print(data_pivot)
		#print(data_store)
		return data_store
		
	except:
		print("Processing Failed!")

def removeAllFiles():
	#shutil.rmtree("/home/runner/JMA-Works/CSV")
	print("Removing Files!")
	for file in os.scandir("/home/runner/JMA-Works/CSV"):
		os.remove(file.path)
		
#def filedAgainst():
#	df=data['Filed Against'].unique()
#	df = pd.DataFrame(data=df)
#	df=df.dropna()
#	#df[0].to_string(index=False)
#	filedAgainst=(df[0].to_list())
#	return filedAgainst		