import pyrebase
from flask import *
from config import Config1

c1 = Config1()

firebase = pyrebase.initialize_app(c1.giveConfig())

auth = firebase.auth()

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
        print(user['idTokens'])
    return "success"


@app.route("/signin-sch",methods = ['POST','GET'])
def signinsch():
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']

        user = auth.sign_in_with_email_and_password(email,password)
        
    return "success"
        
@app.route("/signin-lm",methods = ['POST','GET'])
def signinlm():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = auth.sign_in_with_email_and_password(email,password)
            print(user)
            
            return "successful"

    
        except:
            return "Check your credentials"


if __name__ == "__main__":
    app.run(debug=True)


