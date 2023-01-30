import json
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from dotenv import load_dotenv
import requests
import os
import pyrebase

config = {
    "apiKey": "AIzaSyDE40KdAA7IBVFWZtpoChNn8TnU2ZyIDnQ",
    "authDomain": "weather-app-370205.firebaseapp.com",
    "projectId": "weather-app-370205",
    "storageBucket": "weather-app-370205.appspot.com",
    "messagingSenderId": "32945948648",
    "appId": "1:32945948648:web:a164456149daa1fc2c465d",
    "measurementId": "G-FH4TRV05PG",
    "databaseURL" : " "
} #credentials to connect with firebase

firebase = pyrebase.initialize_app(config) #initialize firebase app
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'


load_dotenv()
global api_key
api_key = os.environ.get('API_KEY1')
print(api_key)


@app.route('/')
def index():
    return redirect(url_for("home", status=0))


@app.route('/<status>')
def home(status):
    return render_template('home.html', isRegistered=status)


@app.route('/register/<status>')
def register(status):
    return render_template('register.html',status=status)

@app.route('/saveUser', methods=['POST','GET'])
def saveUser():
     if request.method == 'POST':
          email = request.form["user_name"]
          password = request.form["password"]
    
          try:
               user = auth.create_user_with_email_and_password(email,password)
          except requests.exceptions.HTTPError as e:
                print(e)
                errJson= e.args[1]
                error = json.loads(errJson)['error']['message']
                if error == "EMAIL_EXISTS":
                     print("Email already exists")
                     return redirect(url_for("home",status=2))
                elif error == "INVALID_EMAIL":
                     print("invalid email address")
                     return redirect(url_for("register",status=2))
                elif error == "MISSING_PASSWORD":
                     print("MISSING_PASSWORD")
                     return redirect(url_for("register",status=4))
                else:
                     print(json.loads(errJson)['error']['message'])

     return redirect(url_for("home", status=1))


@app.route('/login', methods=['POST','GET'])
def loginUser():
    if('user' in session):
        return redirect(url_for("getCity"))
    
    if request.method == 'POST':
      email = request.form["user_name"]
      password = request.form["password"]
    
      try:
           user = auth.sign_in_with_email_and_password(email,password)
           session['user'] = email
      except requests.exceptions.HTTPError as e:
                print(e)
                errJson= e.args[1]
                error = json.loads(errJson)['error']['message']
                
                if error == "INVALID_EMAIL":
                     print("invalid email address")
                     return redirect(url_for("home",status=4))
                elif error == "MISSING_PASSWORD":
                     print("MISSING_PASSWORD")
                     return redirect(url_for("home",status=5))
                elif error == "INVALID_PASSWORD":
                     print("password is invalid")
                     return redirect(url_for("home",status=6))
                else:
                     return redirect(url_for("home",status=5))

    return redirect(url_for("getCity"))


@app.route('/getCity')
def getCity():
    return render_template("weather.html", weather_location="", weather_state="",
                           weather_temperature="", weather_condition="", weather_image="", DNimg="day.png", weather_date="", w_isCityFound=2,user='{}'.format(session['user']))


@app.route('/weather', methods=["POST"])
def weather():
    city = request.form["city"]
    details = {
        "q": city,
        "aqi": "yes",
        "key": api_key
    }

    global response
    response = requests.post(
        url="https://api.weatherapi.com/v1/current.json", data=details)

    if response.status_code != 200:
        return render_template("weather.html", weather_location="", weather_state="",
                               weather_temperature="", weather_condition="", weather_image="", DNimg="day.png", weather_date="", w_isCityFound=1)

    location = response.json()['location']['name']
    state = response.json()['location']['region']
    date = response.json()['location']['localtime']
    temperature = response.json()['current']['temp_c']
    condition = response.json()['current']['condition']['text']
    image = response.json()['current']['condition']['icon']

    print(".....")
    global dayOrNightImg
    if (response.json()['current']['is_day'] == 1):
        dayOrNightImg = "day.png"
    if (response.json()['current']['is_day'] == 0):
        dayOrNightImg = "night.jpg"

    return render_template("weather.html", weather_location=location, weather_state=state,
                           weather_temperature=temperature, weather_condition=condition, weather_image=image, DNimg=dayOrNightImg, weather_date=date, w_isCityFound=0)


@app.route('/hourlyForecast/<city>')
def getHourlyForecast(city):
    f_details = {
        "q": city,
        "aqi": "yes",
        "days": 2,
        "key": api_key
    }
    f_response = requests.post(
        url="https://api.weatherapi.com/v1/forecast.json", data=f_details)
    hourlyForecast = f_response.json()['forecast']['forecastday']
    return render_template("tables.html", data=hourlyForecast)


@app.route('/logout')
def logoutUser():
    session.pop("user")
    return redirect(url_for("home", status=3))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000", debug=True)
