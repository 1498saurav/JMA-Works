from dateutil.parser import parse
import pandas as pd

filename="/home/runner/JMA-Works/CSV/Main.csv"
data=pd.read_csv(filename)

def convert(x):
	dt=parse(x, fuzzy_with_tokens=True)
	return(dt[0].strftime('%m/%d/%Y'))

data["Created Date"]=data["Created Date"].apply(convert)

print(data["Created Date"])