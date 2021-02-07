from flask import Flask, render_template, request, flash, redirect, jsonify
import pickle
import numpy as np
from googleplaces import GooglePlaces, types, lang 



app = Flask(__name__)

def predictHeart(values, dic):
    model = pickle.load(open('Final_Model/heart_final.pkl','rb'))
    values = np.asarray(values)
    return model.predict(values.reshape(1, -1))[0]

def predictKidney(values, dic):
    model = pickle.load(open('Final_Model/kidney_final.pkl','rb'))
    values = np.asarray(values)
    return model.predict(values.reshape(1, -1))[0]

def predictDiabetes(values, dic):
    model = pickle.load(open('Final_Model/diabetes_final.pkl','rb'))
    values = np.asarray(values)
    return model.predict(values.reshape(1, -1))[0]

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/kidney_prediction", methods=['GET', 'POST'])
def kidneyPrediction():
    return render_template('kidney.html')

@app.route("/diabetes_prediction", methods=['GET', 'POST'])
def diabetesPrediction():
    return render_template('diabetes.html')

@app.route("/heart_prediction", methods=['GET', 'POST'])
def heartPrediction():
    return render_template('Heart.html')

@app.route("/heart_disease_predict", methods = ['POST', 'GET'])
def predictHeartDisease():
    try:
        if request.method == 'POST':
            to_predict_dict = request.form.to_dict()
            print(to_predict_dict)
            to_predict_list = list(map(float, list(to_predict_dict.values())))
            print(to_predict_list)
            pred = predictHeart(to_predict_list, to_predict_dict)
            if pred==0:
                heart_prediction='Great, You are Healthy! no heart disease traced'
                
            else:
                heart_prediction='Heart Disease Traced. If you have Symptom, Kindly Seek emergency medical Care immediatly'
                
    except:
        message = "Please enter all parameters of Data"
        return render_template('heartresult.html', status='failure',error=message)
    return render_template('heartresult.html',pred=pred, status = 'success',prediction=heart_prediction,symptoms_of_heart_disease=["Chest pain","Irregular heartbeat","Shortness of breath","Fainting"],suggesstion="Always call 911 or emergency medical help if you think you might be having a heart attack. Heart disease is easier to treat when detected early, so talk to your doctor about your concerns regarding your heart health.")
        

@app.route("/kidney_disease_predict", methods = ['POST', 'GET'])
def predictKidneyDisease():
    try:
        if request.method == 'POST':
            to_predict_dict = request.form.to_dict()
            print(to_predict_dict)
            to_predict_list = list(map(float, list(to_predict_dict.values())))
            print(to_predict_list)
            pred = predictKidney(to_predict_list, to_predict_dict)
            if pred==0:
                kidney_prediction='Great, You are Healthy! No Kidney Disease traced'
                
            else:
                kidney_prediction='Kidney Disease Traced. If you have Symptoms as shown, Kindly Seek emergency medical Care'
                
    except:
        message = "Please enter all parameters of Data"
        return render_template('kidneyresult.html', status='failure',error=message)

    return render_template('kidneyresult.html',pred=pred, status = 'success',prediction=kidney_prediction,symptoms_of_kidney_disease=["weight loss and poor appetite","tiredness","Shortness of breath","blood in your pee (urine)","an increased need to pee – particularly at night "],suggesstion="The symptoms of kidney disease can be caused by many less serious conditions, so it's important to get a proper diagnosis. If you do have CKD, it's best to get it diagnosed as soon as possible. ")


@app.route("/diabetes_predict", methods = ['POST', 'GET'])
def predictDiabetesDisease():
    try:
        if request.method == 'POST':
            to_predict_dict = request.form.to_dict()
            print(to_predict_dict)
            to_predict_list = list(map(float, list(to_predict_dict.values())))
            print(to_predict_list)
            pred = predictKidney(to_predict_list, to_predict_dict)
            if pred==0:
                diabetes_prediction='Great, You are Healthy! No Diabetes traced'
                
            else:
                diabetes_prediction='Diabetes Disease Traced. If you have Symptoms as shown, Kindly Seek emergency medical Care'
                
    except:
        message = "Please enter all parameters of Data"
        return render_template('diabetesresult.html', status='failure',error=message)

    return render_template('diabetesresult.html',pred=pred, status = 'success',prediction=diabetes_prediction,symptoms_of_diabetes=["Lose weight without trying","Are very hungry","Have blurry vision","Are very thirsty","Have blurry vision"],suggesstion="If you're older than 45 or have other risks for diabetes, it's important to get tested. When you spot the condition early, you can avoid nerve damage, heart trouble, and other complications.")
        

@app.route("/find_nearest_hospital", methods = [ 'GET'])
def findNearestHospital():
    try:
        hosp_places=list()
        if request.method == 'GET':
            API_KEY = request.args.get("api_key")
            
            longitude = request.args.get('longitude')
            print(longitude)
            latitude = request.args.get('latitude')
            radius = request.args.get('radius')
            google_places = GooglePlaces(API_KEY)
            query_result = google_places.nearby_search( 
                # lat_lng ={'lat': 46.1667, 'lng': -1.15}, 
                lat_lng ={'lat': latitude, 'lng': longitude}, 
                radius = radius, 
                # types =[types.TYPE_HOSPITAL] or 
                # [types.TYPE_CAFE] or [type.TYPE_BAR] 
                # or [type.TYPE_CASINO]) 
                types =[types.TYPE_HOSPITAL])
            for place in query_result.places:
                hosp_places.append(jsonify(hospital_name=place.name,
                                           Latitude=place.geo_location['lat'],
                                           Longitude=place.place.geo_location['lng']))
                           
    except Exception as e:
        return jsonify(error="Error with API key, Please check if API key is valid and You must enable Billing on the Google Cloud Project at https://console.cloud.google.com/project/_/billing/enable Learn more at https://developers.google.com/maps/gmp-get-started")

    return jsonify(hosp_places)

if __name__ == '__main__':
	app.run(debug = True)
