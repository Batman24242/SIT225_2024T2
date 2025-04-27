import pandas as pd
import firebase_admin
from firebase_admin import db

databaseURL = 'https://arpit-stask-default-rtdb.firebaseio.com/'
cred_obj = firebase_admin.credentials.Certificate(
    'arpit.json'
)

default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':databaseURL
	})

ref = db.reference('/')
data = ref.get()
df = pd.DataFrame(data.values())
df.to_csv('arpit.csv', index = False)