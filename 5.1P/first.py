import serial
import math
import time
from datetime import datetime
import firebase_admin
from firebase_admin import db

databaseURL = 'https://arpit-stask-default-rtdb.firebaseio.com/'
cred_obj = firebase_admin.credentials.Certificate(
    'arpit.json'
)
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':databaseURL
	})

ref = db.reference("/")



ser = serial.Serial('COM5', 9600)

while True:
    try:
        line = ser.readline().decode().strip()
        x_value, y_value, z_value = line.split(',')
        x = float(x_value)
        y = float(y_value)
        z = float(z_value)

        if math.isnan(x) or math.isnan(y) or math.isnan(z):
            continue

        timestamp = datetime.now().isoformat()
        ref.push(
            {
                'Time' : timestamp,
                'x' : x,
                'y' : y,
                'z' : z,
            }
        )

    except Exception as e:
        print(e)
