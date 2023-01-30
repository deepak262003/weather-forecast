import pyrebase

config = {
    "apiKey": "AIzaSyD18AV__wRT5sI5_s6mYXabt6eQ7pZtQuc",
    "authDomain": "citywet-b7750.firebaseapp.com",
    "projectId": "citywet-b7750",
    "storageBucket": "citywet-b7750.appspot.com",
    "messagingSenderId": "1016369633018",
    "appId": "1:1016369633018:web:7f1e0b0b75554ad3321b43",
    "measurementId": "G-D1M8PWRT4D",
    "databaseURL": " "
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = "test@example.com"
password = "123456"

user = auth.create_user_with_email_and_password(email, password)
print(user)

#user = auth.sign_in_with_email_and_password(email, password)


#info = auth.get_account_info(user["idToken"])
#print(info)