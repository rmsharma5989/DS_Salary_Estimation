#import flask
from flask import Flask, jsonify, request
import json
import pickle
from input_file import input_data
import numpy as np


file_name = "models/model_file.p"
def load_models():
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model

app = Flask(__name__)
@app.route('/predict', methods=['GET'])
def predict():
    # get input data
    request_json = request.get_json()
    x = request_json['input_data']
    x_in = np.array(x).reshape(1,-1)
    
    # load model
    model = load_models()
    
    prediction = model.predict(x_in)[0]
    response = json.dumps({'response': prediction})
    return response, 200



@app.route('/test', methods=['GET'])
def test():
    response = json.dumps({'response': 'yahhhh!'})
    return response, 200


if __name__ == '__main__':
    application.run(debug=True)

