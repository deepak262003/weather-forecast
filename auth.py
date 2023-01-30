import pyrebase

config = {
    "apiKey": "AIzaSyDE40KdAA7IBVFWZtpoChNn8TnU2ZyIDnQ",
    "authDomain": "weather-app-370205.firebaseapp.com",
    "projectId": "weather-app-370205",
    "storageBucket": "weather-app-370205.appspot.com",
    "messagingSenderId": "32945948648",
    "appId": "1:32945948648:web:a164456149daa1fc2c465d",
    "measurementId": "G-FH4TRV05PG",
    "databaseURL":""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = "test@example.com"
password = "123456"

#user = auth.create_user_with_email_and_password(email, password)
#print(user)

user = auth.sign_in_with_email_and_password(email, password)


#info = auth.get_account_info(user["idToken"])
#print(info)