from flask import Blueprint, request
import dill as pickle
import csv
import time

predict_api = Blueprint('predict_api', __name__, template_folder='templates')

with open('./API/weather_trained.pk', 'rb') as file1:
    loaded_model_1 = pickle.load(file1)

with open('./API/friction_trained.pk', 'rb') as file2:
    loaded_model_2 = pickle.load(file2)

@predict_api.route('/predict/friction', methods=['GET', 'POST'])
def predict():
    
    data_predict = []
    weather_res = []
    value = 0.0

    if request.method == 'POST':
        response = {}

        data_predict.append(request.form['temp'])
        data_predict.append(request.form['rf'])
        data_predict.append(request.form['hum'])
        data_predict.append(request.form['dewp'])

        prediction = loaded_model_1.predict([data_predict])

        weather_res.append(prediction)
        weather_res.append(request.form['fric'])

        with open('./API/pred_results.pk', 'wb') as f:
            pickle.dump(weather_res, f)

        response = "ok, check the app"

        return response
    
    elif request.method == 'GET':
        with open('./API/pred_results.pk', 'rb') as f1:
            weather_res = pickle.load(f1)       

        if len(weather_res) == 2:
            result = loaded_model_2.predict([weather_res])

            value = result[0]

        else:
            with open('./API/fric_value.pk', 'rb') as f2:
                friction_val = pickle.load(f2)

            weather_res.append(friction_val)

            result = loaded_model_2.predict([weather_res])

            value = result[0]
            
        return value