# importar os pacotes
import flask
import pandas as pd
import pickle 
import numpy as np

# importar modelo e feature names
with open('model/modelo_simples.pkl', 'rb') as file:
	modelo_simples = pickle.load(file)

with open('model/features_simples.names', 'rb') as file:
    features_names = pickle.load(file)


app = flask.Flask(__name__, template_folder="templates")

@app.route("/", methods=['GET', 'POST'])


def main():

	if flask.request.method == 'GET':
		return flask.render_template("home.html",valor_venda=0)

	if flask.request.method == 'POST':
		# verificando o que foi digitado
		user_inputs = {
			"Condo": flask.request.form["condominio"],
			"Size": flask.request.form["area"],
			"Rooms": flask.request.form["quartos"],
			"Suites": flask.request.form["suites"]
		}
	
		# input para dataframe (em branco)
		df = pd.DataFrame(index=[0], columns=features_names)
		df = df.fillna(value=0)

		for i in user_inputs.items():
			df[i[0]] = i[1]

		df = df.astype(float)

		var_area = int(df[['Size']].iloc[0].values)
		var_condo = int(df[['Condo']].iloc[0].values)
		var_rooms = int(df[['Rooms']].iloc[0].values)
		var_suites = int(df[['Suites']].iloc[0].values)

		# fazendo a previsao
		y_pred = float(modelo_simples.predict(df)[0])

		return flask.render_template("home.html", valor_venda=y_pred, 
									disp_area = var_area, 
									disp_condo=var_condo, 
									disp_rooms=var_rooms, 
									disp_suites=var_suites)
	

if __name__ == "__main__" :
	#app.run(host='127.0.0.1',debug=True)
	app.run()


