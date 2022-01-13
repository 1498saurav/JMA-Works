import pandas as pd

member=[
'Atharv',
'Swarnima',
'Piyush22',
'Deepak201',
'Ankita.Shinde',
'Snehal1',
'Namrata',
'Komal',
'Chandan',
'Premkumar',
'Nikhil',
'Ashish20',
'Khushboo1',
'Roopesh',
'Somesh',
'Tanmay',
'Vedant',
'Aparna',
'Ankita3'
]

def products():
	filename="/home/runner/JMA-Works/CSV/Main.csv"
	data=pd.read_csv(filename)
	df=data['Filed Against'].unique()
	df = pd.DataFrame(data=df)
	df=df.dropna()
	filedAgainst=(df[0].to_list())
	return filedAgainst