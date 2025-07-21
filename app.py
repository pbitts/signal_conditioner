from flask import Flask, render_template, request
from signal_conditioner import Conditioner  

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calcular():
    vin_min = float(request.form['vin_min'])
    vin_max = float(request.form['vin_max'])
    vout_min = float(request.form['vout_min'])
    vout_max = float(request.form['vout_max'])
    max_tries = int(request.form['iterations'])

    conditioner = Conditioner(desired_output_signal=[vout_max, vout_min], 
                        input_signal_rms = [vin_max, vin_min], 
                        max_tries=max_tries)

    return render_template('result.html', result=conditioner.chosen_circuits)

if __name__ == '__main__':
    app.run(debug=True)
