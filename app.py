import pyrebase
from flask import *
from config import Config1
from formula import distpy
import geopy.distance

c1 = Config1()

firebase = pyrebase.initialize_app(c1.giveConfig())

auth = firebase.auth()

db = firebase.database()

app = Flask("__main__")

app.config['SECRET_KEY'] = 'loopedu'

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
        session['l_uid'] = user['localId']
        db.child("loopman").child(user['localId']).child().set({
            "name": name,
            "email": email,
            "number": number
        
        })
        return redirect('/admin/dashboard')
    return render_template("signinall.html")
#3cByf1KR2xbTzpaIB8JOkEEqCxt1

@app.route("/signin-sch",methods = ['POST','GET'])
def signins_ch():
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']

        user = auth.sign_in_with_email_and_password(email,password)
        session['s_uid'] = user['localId']

    return "success"
        
@app.route("/signin-lm",methods = ['POST','GET'])
def signin_lm():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = auth.sign_in_with_email_and_password(email,password)
            session['l_uid'] = user['localId']
            print(session['l_uid'])
            return redirect('/admin/dashboard')

    
        except:
            print('login error')
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
        u_idx = user['loaclId']
        print(u_idx)

        db.child("schools").child(u_idx).child().set({
            "name": school_name,
            "email": email,
            "number": number,
            "principle": principal,
            "incharge": incharge,
            "pincode": pincode,
            "address": address,
            "cluster": cluster,
            "lat": lat,
            "lon": lon,
            "u_id": u_idx
        })
        session['s_uid'] = user['localId']
        return render_template("loopdash.html")

    return render_template("schoolRegistration.html")

@app.route("/loop")
def loopdash():
    return render_template("loopdash.html")

@app.route("/admin/dashboard", methods=['POST', 'GET'])
def lpdashboard():
    if request.method == 'GET':
        return render_template("loopdash.html")

@app.route("/admin/verify_resources")
def verifyresources():
    return render_template("verify_resources.html")


@app.route("/admin/cluster", methods=['POST','GET'])
def lpclusterform():

    if request.method == 'POST':
        schools = db.child("schools").get().val()
        scls = []
        lplat = float(request.form['lat'])
        lplong = float(request.form['long'])
        radius = float(request.form['radius'])
        for i in schools.values():
            if i['cluster'] != None and i['cluster']!= 'yes':
                coords_1 = (lplat,lplong)
                coords_2 = (float(i['lat']), float(i['lon']))
                if geopy.distance.vincenty(coords_1, coords_2) <= radius:
                    print(geopy.distance.vincenty(coords_1, coords_2))
                    scls.append(i)
            print(scls)
        return render_template("schools_list.html", scls = scls)
    return render_template("clusterform.html")

@app.route("/admin/cluster/schools_list",methods=['POST','GET'])
def selectschools():
    if request.method == 'POST':
        selected = request.form.getlist('listofschools')
        print(selected)
        sel_list = []
        for i in selected:
            sel_list.append(i)
        c_name = request.form['cname']
        d = {
            "c_name":c_name,
            "schools_present":sel_list,
            "school_count":len(sel_list)
        }
        print(sel_list)
        ref = db.child("clusters").push(d)
        clust_id = ref['name']
        for school in sel_list:
            db.child('schools').child(school).update({
            "cluster":"yes",
            "clust_id":clust_id
            })
        return redirect('/admin/dashboard')
    return render_template("schools_list.html")


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


