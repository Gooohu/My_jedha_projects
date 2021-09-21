from flask import Flask,request, url_for, redirect, render_template, jsonify
import requests
import pandas as pd
import pickle
import numpy as np
import joblib

app = Flask(__name__)

# Load model
classifier = joblib.load("model.joblib")
print(" * Model loaded!")

cols=['fixed acidity', 'volatile acidity', 'citric acid','residual sugar', 'chlorides', 'free sulfur dioxide','total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol']

@app.route("/")
def home():
    return render_template("index.html")

#Our page which will predict in live
@app.route('/predict_live',methods=['POST'])
def predict_live():
    #For rendering results on HTML GUI
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = classifier.predict(final_features)
    output = round(prediction[0], 2) 
    return render_template('index.html', prediction_text='We predict a quality of this wine around :{}/10'.format(output))

#Our page which will predict through an API
@app.route("/predict", methods=["POST"])
def index():
    # Get the data
    req = request.get_json()
         # Predict
    prediction = classifier.predict( [req[key] for key in req.keys()] )
    print('prediction done')
        # Return the result as JSON but first we need to transform the
        # result so as to be serializable by jsonify()
    prediction = [ str(round(prediction[i],0)) for i in range(len(prediction)) ] 
    return jsonify({"predict": prediction}), 200
    return jsonify({"msg": POST_error(req)[1]})
    

if __name__ == "__main__":
    app.run(debug=True)