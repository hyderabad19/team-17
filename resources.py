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
        name = formdata['r_name']
        desp = formdata['description']
        capacity = formdata['capacity']
        categ = formdata['categ']
        if 's_uid' in session:
            uid = session['s_uid']
            avail = True
            db.child('schools').child(uid).child('resources').child().set({
                "name":name,
                "desp":desp,
                "capacity":capacity,
                "category":categ,
                "avail":avail
            })
        else:
            return redirect('/landing')
        return redirect('/home/resource')
    elif request.method == 'GET':
        return render_template('resource_add.html')


@app.route('/home/resource')
def show_resource():
    #list of resources
    if 's_uid' in session:
        resources = db.child('schools').child(session['s_uid']).get().val()
        res = []
        for i in resources.values():
            m = i.values()
            res.append(m)
        return render_template('resource.html',res = res)
    else:
        return redirect('/landing')
    return render_template('resource.html')

if __name__ == "__main__":
    app.run(debug=True)