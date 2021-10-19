from dateutil.parser import parse
import pandas as pd
import numpy as np

filename="/home/runner/JMA-Works/CSV/Main.csv"
data=pd.read_csv(filename)

def convert(x):
	dt=parse(x, fuzzy_with_tokens=True)
	return (dt[0].strftime("%Y-%m-%d"))

def test():
	data["Created Date"]=data["Created Date"].apply(convert)
	data['Created Date'] = pd.to_datetime(data['Created Date'])
	return data

data=test()

start_date = '2021-09-01'
end_date = '2021-10-19'
mask = (data['Created Date'] >= start_date) & (data['Created Date'] <= end_date)
data = data.loc[mask]
print(data)

