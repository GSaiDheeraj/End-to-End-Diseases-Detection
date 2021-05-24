from flask import Flask, render_template, url_for, flash, redirect
from flask import request
from flask import send_from_directory
from flask_socketio import SocketIO

import numpy as np
import tensorflow
from tensorflow import keras
import tensorflow as tf
import os
from tensorflow.keras.models import load_model


#from this import SQLAlchemy
app=Flask(__name__,template_folder='template')


app.config['SECRET_KEY'] = "UddA58IkCqP5nZkwEzA7YA"



dir_path = os.path.dirname(os.path.realpath(__file__))
# UPLOAD_FOLDER = dir_path + '/uploads'
# STATIC_FOLDER = dir_path + '/static'
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'



#global graph
#graph = tf.get_default_graph()
model = tensorflow.keras.models.load_model('model111.h5')
model1 = tensorflow.keras.models.load_model("pneumonia.h5")
model2 = tensorflow.keras.models.load_model("Covid_model.h5")
model3 = tensorflow.keras.models.load_model("CovidCT_model.h5")


# Malaria
def api(full_path):
    #with graph.as_default():
    data = keras.preprocessing.image.load_img(full_path, target_size=(50, 50, 3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0 / 255
        #with graph.as_default():
    predicted = model.predict(data)
    return predicted
#pneumonia
def api1(full_path):
    #with graph.as_default():
    data = keras.preprocessing.image.load_img(full_path, target_size=(224, 224, 3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0/ 255
    predicted = model2.predict(data)
    return predicted

#Covid-19
def api111(full_path):
    #with graph.as_default():
    data = keras.preprocessing.image.load_img(full_path, target_size=(224, 224, 3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0/ 255
    predicted = model2.predict(data)
    return predicted
def api1111(full_path):
    #with graph.as_default():
    data = keras.preprocessing.image.load_img(full_path, target_size=(224, 224, 3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0/ 255
    predicted = model3.predict(data)
    return predicted

# Malaria
@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    #with graph.as_default():
    if request.method == 'GET':
        return render_template('malaria.html')
    else:
        try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)

            indices = {0: 'PARASITIC', 1: 'Uninfected'}
            result = api(full_name)
            print(result)

            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(result[0][predicted_class] * 100, 2)
            label = indices[predicted_class]
            if accuracy<85:
                prediction = "Please, Check with the Doctor."
            else:
                prediction = "Result is accurate"

            return render_template('malariapredict.html', image_file_name=file.filename, label=label, accuracy=accuracy, prediction=prediction)
        except:
            flash("Please select the image first !!", "danger")
            return redirect(url_for("Malaria"))

#Pneumonia
@app.route('/upload11', methods=['POST', 'GET'])
def upload11_file():
    #with graph.as_default():
    if request.method == 'GET':
        return render_template('pneumonia.html')
    else:
        try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)
            indices = {1: 'Healthy', 0: 'Pneumonia-Infected'}
            result = api1(full_name)
            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(result[0][predicted_class] * 100, 2)
            label = indices[predicted_class]
            if accuracy < 85:
                prediction = "Please, Check with the Doctor."
            else:
                prediction = "Result is accurate"

            return render_template('pneumoniapredict.html', image_file_name=file.filename, label=label, accuracy=accuracy,
                                   prediction=prediction)
        except:
            flash("Please select the X-ray image first !!", "danger")
            return redirect(url_for("Pneumonia"))

#Covid-19
@app.route('/upload111', methods=['POST', 'GET'])
def upload111_file():
    #with graph.as_default():
    if request.method == 'GET':
        return render_template('corona.html')
    else:
        try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)
            indices = {1: 'Healthy', 0: 'Corona-Infected'}
            result = api111(full_name)
            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(result[0][predicted_class] * 100, 2)
            label = indices[predicted_class]
            if accuracy<85:
                prediction = "Please, Check with the Doctor."
            else:
                prediction = "Result is accurate"

            return render_template('coronapredict.html', image_file_name = file.filename, label = label, accuracy = accuracy, prediction=prediction)
        except:
            flash("Please select the X-ray image first !!", "danger")
            return redirect(url_for("covid_19"))

@app.route('/upload1111', methods=['POST', 'GET'])
def upload1111_file():
    #with graph.as_default():
    if request.method == 'GET':
        return render_template('corona1.html')
    else:
        try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)
            indices = {1: 'Healthy', 0: 'Corona-Infected'}
            result = api1111(full_name)
            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(result[0][predicted_class] * 100, 2)
            label = indices[predicted_class]
            if accuracy<85:
                prediction = "Please, Check with the Doctor."
            else:
                prediction = "Result is accurate"

            return render_template('coronapredict1.html', image_file_name = file.filename, label = label, accuracy = accuracy, prediction=prediction)
        except:
            flash("Please select the CT-Scan image first !!", "danger")
            return redirect(url_for("covidct_19"))
	
@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

#logged in Home page
@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def login1():
    return render_template("signup.html")

@app.route("/home")
def index2():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/covid_19")
def covid_19():
    # if form.validate_on_submit():
    return render_template("corona.html")

@app.route("/covidct_19")
def covidct_19():
    return render_template("corona1.html")

@app.route("/Malaria")
def Malaria():
    return render_template("malaria.html")

@app.route("/Pneumonia")
def Pneumonia():
    return render_template("pneumonia.html")


if __name__ == "__main__":
	app.run(debug=True)
