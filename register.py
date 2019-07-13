import pyrebase
from flask import *
from config import Config1

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
        u_idx = user['loaclId']
        print(u_idx])
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
        return render_template("schoolRegistration.html")

    return render_template("schoolRegistration.html")

@app.route("/loop")
def loopdash():
    return render_template("loopdash.html")

if __name__ == "__main__":
    app.run(debug=True)


