import pandas as pd

def products():
	filename="/home/runner/JMA-Works/CSV/Main.csv"
	data=pd.read_csv(filename)
	df=data['Filed Against'].unique()
	df = pd.DataFrame(data=df)
	df=df.dropna()
	filedAgainst=(df[0].to_list())
	return filedAgainst