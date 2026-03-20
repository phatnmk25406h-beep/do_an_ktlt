import pyrebase

config = {
    "apiKey": "AIzaSyB75TxAPMSv9e__3Poql_fiCpx3XVW6zTU",
    "authDomain": "m3m-english.firebaseapp.com",
    "projectId": "m3m-english",
    "storageBucket": "m3m-english.firebasestorage.app",
    "messagingSenderId": "529571980593",
    "appId": "1:529571980593:web:8c32e11576a1d2d6a73c10",
    "measurementId": "G-B9ZFE1G1EG",
    "databaseURL": "https://m3m-english-default-rtdb.asia-southeast1.firebasedatabase.app/"  
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()