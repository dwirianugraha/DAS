from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
from helper import *

matplotlib.use('Agg')

app = Flask(__name__)

data = load_data()

@app.route("/")
def index():
	# generate value for cards
	percent_fraud = float((pd.crosstab(index=data['fraud_reported'],columns='count',normalize=True)).loc['Y', 'count']*100)
	fraud_loss = pd.crosstab(index=data['fraud_reported'],columns='jumlah',values= data['total_claim_amount'], aggfunc='sum').loc['Y', 'jumlah']
	average_claim = data['total_claim_amount'].median()
	
	# generate value Fraud Data from Severity Report
	percent_Severity_Major_fraud = round(float((pd.crosstab(index=(data[data.fraud_reported == 'Y'])['incident_severity'],columns='count',normalize=True)).loc['Major Damage', 'count']*100),2)
	#------------------------------------------------
	Claim_Fraud = data[data.fraud_reported == 'Y'].pivot_table(index='incident_severity',values='fraud_reported',aggfunc='count')
	Claim_All = data.pivot_table(index='incident_severity',values='fraud_reported',aggfunc='count')
	Kontribusi_Fraud = round((Claim_Fraud/Claim_All*100).loc['Major Damage', 'fraud_reported'],2)
	#------------------------------------------------
	Severity_HighRisk = data[data.fraud_reported == 'Y'].pivot_table(index='incident_severity',values='fraud_reported',aggfunc='count').sort_values('fraud_reported', ascending=False).reset_index().iloc[0 , 0]
	Severity_LowRisk = data[data.fraud_reported == 'Y'].pivot_table(index='incident_severity',values='fraud_reported',aggfunc='count').sort_values('fraud_reported', ascending=True).reset_index().iloc[0 , 0]
	
	# generate value Fraud Data from Property Damage
	Fraud_Property_Damage = round(float((pd.crosstab(index=(data[data.fraud_reported == 'Y'])['property_damage'],columns='count',normalize=True)).loc['?', 'count']*100),2)
	
	# compile card values as card_data
	card_data = dict(
		percent_fraud = f'{percent_fraud}%',
		fraud_loss = f'US$ {fraud_loss:,}',
		average_claim = f'US$ {average_claim:,}',
		percent_Severity_Major_fraud = f'{percent_Severity_Major_fraud}%',
		Kontribusi_Fraud = f'{Kontribusi_Fraud}%',
		Severity_HighRisk = Severity_HighRisk,
		Severity_LowRisk = Severity_LowRisk,
		Fraud_Property_Damage = f'{Fraud_Property_Damage}%'
	)

	# generate plot
	plot_age_res = plot_age(data)
	plot_premium_res = plot_premium(data)
	plot_incident_res = plot_incident(data)
	plot_report_res = plot_report(data)
	plot_severity_res = plot_severity(data)
	plot_incidenttype_res = plot_incidenttype(data)
	plot_education_res = plot_education(data)

	# render to html
	return render_template('index.html',
		  card_data = card_data, 
		  plot_age_res = plot_age_res,
		  plot_premium_res = plot_premium_res,
		  plot_incident_res = plot_incident_res,
		  plot_report_res = plot_report_res,
		  plot_severity_res = plot_severity_res,
		  plot_incidenttype_res = plot_incidenttype_res,
		  plot_education_res = plot_education_res
		)


if __name__ == "__main__": 
    app.run(debug=True)
