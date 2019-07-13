from flask import *
import pyrebase
from config import Config1
from formula import distpy

c1 = Config1
app = Flask("__main__")
firebase = pyrebase.initialize(c1.giveConfig())
db = firebase.database()
@app.route("/admin/dashboard", methods=['POST', 'GET'])
def lpdashboard():
    return render_template("m1.html")


@app.route("/admin/clusterform")
def lpclusterform():
    render_template("clusterform.html")


@app.route("/admin/verify_resources")
def verifyresources():
    render_template("verify_resources.html")


@app.route("/admin/cluster/list_of_schools", methods=['POST','GET'])
def lpclusterform():
    schools = db.child("schools").get().val()
    scls = []
    if request.method == 'POST':
        if request.form['submit'] == 'add':
            lplat = request.form['lat']
            lplong = request.form['long']
            radius = request.form['radius']
            for i in schools.values():
                if i.values()['inCluster'] != None and i.values()['inCluster']!= 'yes':
                    if distpy(lplat,i['latitude'],lplong,i['longitude']) <= radius:
                        scls.append(i.values())
            return render_template("m1.html", scls = scls)






if __name__ == "__main__":
    app.run(debug = True)
