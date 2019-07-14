import pyrebase
from flask import *
from config import Config1
from formula import distpy
import geopy.distance
from mailsender1 import sendM
c1 = Config1()

firebase = pyrebase.initialize_app(c1.giveConfig())

auth = firebase.auth()

db = firebase.database()

store = firebase.storage()

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
        print(session['s_uid'])
    return redirect('/home/dashboard')

        
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
        u_idx = user['localId']
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
        return redirect('/admin/dashboard')

    return render_template("schoolRegistration.html")

@app.route("/loop")
def loopdash():
    return render_template("loopdash.html")

@app.route("/admin/dashboard", methods=['POST', 'GET'])
def lpdashboard():
    if request.method == 'GET':
        cluster = db.child("clusters").shallow().get()
        clus_key = cluster.val()
        keyList = [i for i in list(clus_key)]
        lis=[]
        for i in keyList:
            clust_e = db.child("clusters").child(i).get().val()
            li1=[]
            li1.append(clust_e['c_name'])
            names = []
            for j in clust_e['schools_present']:
                x = db.child("schools").child(j).get().val()
                names.append(x['name'])
            li1.append(names)
            lis.append(li1)
        return render_template("loopdash.html",clus = lis)


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

@app.route('/logout')
def signOut():
    session.pop('l_uid')
    return redirect('/')

@app.route('/logout_stu')
def signOut2():
    session.pop('s_uid')
    return redirect('/')

@app.route('/home/resource/',methods=['POST','GET'])
def add_resource():
    if request.method == 'POST':
        formdata = request.form
        print(formdata)
        name = formdata['r_name']
        desp = formdata['description']
        capacity = formdata['capacity']
        categ = formdata['categ']
        f = request.files['r_image']
        fname = f.filename
        if 's_uid' in session:
            uid = session['s_uid']
            avail = True
            fire_ref = store.child(u'resources').child(fname).put(f)
            link = store.child(u'resources').child(fname).get_url(None)
            ref = db.child('schools').child(uid).child('resources').child().push({
                "name":name,
                "desp":desp,
                "capacity":capacity,
                "category":categ,
                "avail":avail,
                "verified":False,
                "url":link
            })
            print(ref['name'])
            db.child('loopman').child('Q7F9y3WfP4VONOlNoLYTzJuHjSw2').child('requests').push({
                "sch_uid":session['s_uid'],
                "res_id":ref['name']
            })
            school = db.child("schools").child(uid).get().val()
            sendM('Hey Loop Manager! You\'ve got a resource request!',school['name'] + ' have submitted a request for their resource '+ name + '<br><a href="localhost:5000/signin" >Verify Now!</a>',['loopedu123@gmail.com'])
            return redirect('/home/resource')
    elif request.method == 'GET':
        return render_template('resource_add.html')


@app.route('/home/dashboard')
def show_resource():
    #list of resources
    if 's_uid' in session:
        school_data = db.child('schools').child(session['s_uid']).get().val()
        resources = db.child('schools').child(session['s_uid']).child('resources').get().val()
        res = []
        if resources != None:
            for i in resources.values():
                res.append(i)
            print(res)
            return render_template('school_dashboard.html',school=school_data,res=res)
        return render_template('school_dashboard.html',school = school_data)
    else:
        return redirect('/landing')
    return render_template('school_dashboard.html')

@app.route('/home/dashboard/book_slot',methods=['GET','POST'])
def book_slot():
    week = {
        'monday':1,
        'tuesday':2,
        'wednesday':3,
        'thursday':4,
        'friday': 5,
        'saturday': 6,
        'sunday': 7}


    if request.method == 'POST':
        fday = request.form['fday']
        lday = request.form['lday']
        
        fnum = week[fday]
        lnum = week[lday]

        

        
    return render_template("book_slot.html")
@app.route("/admin/verify_resources/", methods=['POST','GET'])
def verify_r():
    g = db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child("requests").shallow().get()
    f = []
    if g.val():
        for i in g.val():
            v = db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child("requests").child(i).get()
            h = db.child("schools").child(v.val()['sch_uid']).get()
            j = db.child('schools').child(v.val()['sch_uid']).child("resources").child(v.val()['res_id']).get()
            if 'url' in j.val():
                f.append({'resid':i,'data': {'sname':h.val()['name'], 'resname':j.val()['name'],'url':j.val()['url']}})
            else:
                f.append({'resid':i,'data': {'sname':h.val()['name'], 'resname':j.val()['name']}})
        return render_template("verify_resources.html", f = f,len = len(f))
    else:
        return render_template("verify_resources.html",text="No requests!")

@app.route("/admin/verify_resources/accept/<i>")
def accept(i):
    if i:
        re = db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child("requests").child(i).get().val()
        resource = db.child("schools").child(re['sch_uid']).child("resources").child(re['res_id']).get().val()
        school = db.child("schools").child(re['sch_uid']).get().val()
        db.child("schools").child(re['sch_uid']).child("resources").child(re['res_id']).update({
        "verified":True
        })
        sendM('Hey '+school['name'] +'! You\'re resource has been verified!',resource['name'] + ' has been verified and can be viewed and booked by other schools in your cluster',[school['email']])
        db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child("requests").child(i).remove()
        return redirect("/admin/verify_resources/")

@app.route("/admin/verify_resources/decline/<i>")
def decline(i):
    if i:
        re = db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child("requests").child(i).get().val()
        resource = db.child("schools").child(re['sch_uid']).child("resources").child(re['res_id']).get().val()
        school = db.child("schools").child(re['sch_uid']).get().val()
        db.child("loopman").child("Q7F9y3WfP4VONOlNoLYTzJuHjSw2").child("requests").child(i).remove()
        sendM('Hey '+school['name'] +'! You\'re resource has been rejected :(',resource['name'] + ' has been rejected by the Loop Manager. Contact them to investigate into this',[school['email']])
        return redirect("/admin/verify_resources")



if __name__ == "__main__":
    app.run(debug=True)


