#import shutil
import os
import pandas as pd
import numpy as np

def processData():
	try:
		filename=""

		for file in os.scandir("/home/runner/JMA-Works/CSV"):
			filename=file.path

		data=pd.read_csv(filename)
		data_pivot=pd.pivot_table(data,index="State",columns="Severity",values="Due Date",aggfunc=len,fill_value=0)
		data_pivot["Grand Total"] = data_pivot.sum(axis=1)
		data_pivot.loc["Grand Total"] = data_pivot.select_dtypes(pd.np.number).sum()
		
		#data_pivot=data_pivot.crosstab(Sever, rownames=['a'], colnames=['b', 'c'])
		#pd.crosstab(a, [b, c], rownames=['a'], colnames=['b', 'c'])
		print("Processing data_pivot!")
		print(data_pivot)
		return data_pivot
		
	except:
		print("Processing Failed!")

def removeAllFiles():
	#shutil.rmtree("/home/runner/JMA-Works/CSV")
	print("Removing Files!")
	for file in os.scandir("/home/runner/JMA-Works/CSV"):
		os.remove(file.path)
		