from flask import *
import pyrebase
from config import Config1

c1 = Config1()

app = Flask(__name__)

firebase = pyrebase.initialize_app(c1.giveConfig())

db = firebase.database()

@app.route('/home/resource/submit',methods=['POST','GET'])
def add_resource():
    if request.method == 'POST':
        formdata = request.form
        return redirect('/home/resource')
    elif request.method == 'GET':
        return render_template('resource_add.html')


@app.route('/home/resource')
def show_resource():
    #list of resources
    return render_template('resource.html')

if __name__ == "__main__":
    app.run(debug=True)