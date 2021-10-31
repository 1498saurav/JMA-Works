from datetime import datetime
import pandas as pd

#today = datetime.today().strftime('%Y-%m-%d')
#date_format = '%Y-%m-%d'
#dtObj = datetime.strptime(today, date_format)
#past_date = dtObj - pd.DateOffset(months=4)
#ast_date=past_date.strftime(date_format)

#print(past_date)

def quarter():
	today = datetime.today().strftime('%Y-%m-%d')
	date_format = '%Y-%m-%d'
	dtObj = datetime.strptime(today, date_format)
	past_date = dtObj - pd.DateOffset(months=3)
	past_date=past_date.strftime(date_format)
	return past_date