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
    return render_template("lpanalytics.html")

@app.route("/admin/verify_resources")
def verifyresources():
    render_template("verify_resources.html")


@app.route("/admin/cluster", methods=['POST','GET'])
def lpclusterform():

    if request.method == 'POST':
        if request.form['submit'] == 'add':
            schools = db.child("schools").get().val()
            scls = []
            lplat = request.form['lat']
            lplong = request.form['long']
            radius = request.form['radius']
            for i in schools.values():
                if i.values()['inCluster'] != None and i.values()['inCluster']!= 'yes':
                    if distpy(lplat,i['latitude'],lplong,i['longitude']) <= radius:
                        scls.append(i.values())
            return render_template("schools_list.html", scls = scls)
    return redirect("clusterform.html")

@app.route("/admin/cluster/schools_list")
def selectschools():
    if request.method == 'POST':
        selected = request.form['listofschools']
        sel_list = []
        for i in selected:
            sel_list.append(i)
        c_name = request.form['cname']
        d = dict()
        d['c_name'] = c_name
        d['schools_present'] = sel_list
        d['school_count'] = len(sel_list)
        ref = db.child("clusters").push(d)
        clust_id = ref['name']
        for school in sel_list:
            db.child('schools').child(school).update({
            "inCluster":"yes",
            "clust_id":clust_id
            })
        return redirect('/admin/dashboard')

@app.route("/admin/verify_resources", methods=['POST','GET'])
def verifyresources():
    if request.method == 'POST':
        return redirect("admin/cluster")
    g = db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child("requests").shallow().get()
    f = []
    for i in g.val():
        v = db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child("requests").child(i).get()
        h = db.child("schools").child(v.val()['scid']).get()
        j = db.child("resources").child(v.val()['resid']).get()
        f.append({i, {'sname':h.val()['name'], 'resname':j.val()['name']}})
    return render_template("verify_resources.html", f = f)

@app.route("/admin/verify_resources/accept/<i>")
def accept(i):
    if i not None:
        re = db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child("requests").child(i).get().val()
        resource = db.child("schools").child(re['sch_id']).child("resources").child(re['res_id']).get().val()
        school = db.child("schools").child(re['sch_id']).get().val()
        child("schools").child(re['scid']).child("resources").child(re['res_id']).update({
        "verified":True
        })
        db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child("requests").child(i).remove()
        return render_template("verify_resources.html")

@app.route("/admin/verify_resources/decline/<i>")
def decline(i):
    if i not None:
        re = db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child("requests").child(i).get().val()
        resource = db.child("schools").child(re['sch_id']).child("resources").child(re['res_id']).get().val()
        school = db.child("schools").child(re['sch_id']).get().val()
        db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child("requests").child(i).remove()
        return render_template("verify_resources.html")
if __name__ == "__main__":
    app.run(debug = True)
