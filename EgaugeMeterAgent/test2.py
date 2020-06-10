import pyrebase
import random
import time
config = {
    "apiKey": "AIzaSyBp8zIkQHu5YQBbNIyzF4jjmgne4qJn9q4",
    "authDomain": "peasbhmsr.firebaseapp.com",
    "databaseURL": "https://peasbhmsr.firebaseio.com",
    "storageBucket": "bucket.appspot.com",
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()





