import pyrebase
from flask import *
from config import Config1
from formula import distpy

c1 = Config1()

firebase = pyrebase.initialize_app(c1.giveConfig())

auth = firebase.auth()

db = firebase.database()

app = Flask("__main__")



@app.route("/",methods = ['POST','GET'])
def home():
   return render_template("landing.html")

@app.route("/signinall")
def signinall():
    return render_template("signinall.html")
@app.route("/register",methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        number = request.form['number']
        user = auth.create_user_with_email_and_password(email,password)
        #auth.send_email_verification(user['idToken'])
        
        #user = auth.sign_in_with_email_and_password(email,password)
        print(user['localId'])
        db.child("loopman").child(user['localId']).child().set({
            "name": name,
            "email": email,
            "number": number
        
        })
        return render_template("signinall.html")
    return render_template("signinall.html")
#3cByf1KR2xbTzpaIB8JOkEEqCxt1

@app.route("/signin-sch",methods = ['POST','GET'])
def signins_ch():
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']

        user = auth.sign_in_with_email_and_password(email,password)

    return "success"
        
@app.route("/signin-lm",methods = ['POST','GET'])
def signin_lm():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = auth.sign_in_with_email_and_password(email,password)
            print(user)
            
            return render_template("signinall.html")

    
        except:
            return render_template("signinall.html")

@app.route("/reg-school",methods=["POST","GET"])
def reg_school():
    if request.method == 'POST':
        school_name = request.form['sname']
        principal = request.form['pname']
        incharge = request.form['iname']
        number = request.form['number']
        email = request.form['email']
        address = request.form['address']
        pincode = request.form['pin']
        password = request.form['password']
        cluster = request.form['cluster']
        lat = request.form['lat']
        lon = request.form['lon']
        user = auth.create_user_with_email_and_password(email,password)
        print(user['localId'])
        db.child("schools").child(user['localId']).child().set({
            "name": school_name,
            "email": email,
            "number": number,
            "principle": principal,
            "incharge": incharge,
            "pincode": pincode,
            "address": address,
            "cluster": cluster,
            "lat": lat,
            "lon": lon 
        })
        return render_template("schoolRegistration.html")

    return render_template("schoolRegistration.html")

@app.route("/loop")
def loopdash():
    return render_template("loopdash.html")

@app.route("/admin/dashboard", methods=['POST', 'GET'])
def lpdashboard():
    return render_template("lpanalytics.html")

@app.route("/admin/verify_resources")
def verifyresources():
    return render_template("verify_resources.html")


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

        ref = db.child("clusters").push(d)
        clust_id = ref['name']
        for school in sel_list:
            db.child('schools').child(school).update({
            "inCluster":"yes",
            "clust_id":clust_id
            })
        return redirect('/admin/dashboard')


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
            ref = db.child('schools').child(uid).child('resources').child().push()
            ref.set({
                "name":name,
                "desp":desp,
                "capacity":capacity,
                "category":categ,
                "avail":avail,
                "verified":False
            })
            db.child('loopman').child('Q7F9y3WfP4VONOlNoLYTzJuHjSw2').child('requests').push({
                "sch_uid":session['s_uid'],
                "res_id":ref['name']
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
        return render_template('school_dashboard.html',res = res)
    else:
        return redirect('/landing')
    return render_template('school_dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)

