from flask import *
import pyrebase
from config import Config1
from formula import distpy

c1 = Config1()
app = Flask("__main__")
firebase = pyrebase.initialize_app(c1.giveConfig())
db = firebase.database()
requests_rec = db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child('requests').shallow().get()
reqs = db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child('requests').get()

for i in requests_rec:
    print(i)