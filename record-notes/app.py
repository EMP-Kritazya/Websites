from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "kIhas@1jnmas}a}[asd]!!|aq1h28856565562"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    thing1 = db.Column(db.String(10000))
    thing2 = db.Column(db.String(10000))
    thing3 = db.Column(db.String(10000))
    thing4 = db.Column(db.String(10000))
    thing5 = db.Column(db.String(10000))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def get_in():
    if "name" in session and "email" in session:
        return redirect(url_for("home"))
    else:
        print("Session: ", session)
        return render_template("getin.html")

@app.route("/signup")
def sign_up():
    if "name" in session and "email" in session:
        return redirect(url_for("home"))
    else:
        return render_template("signup.html")

@app.route("/verifySignup", methods = ["POST", "GET"])
def verifySignup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        existing_name = Users.query.filter_by(name=name).first()
        existing_email = Users.query.filter_by(email = email).first()

        if existing_name:
            flash("This name already exists")
            return redirect(url_for("sign_up"))
        elif existing_email:
            flash("This email already exists")
            return redirect(url_for("sign_up"))
        else:
            new_user = Users(name, email)
            db.session.add(new_user)
            db.session.commit()
            flash("Signed In Successfully")
            return redirect(url_for("login"))
    else:
        return redirect(url_for("get_in"))

@app.route("/login")
def login():
    if "name" in session and "email" in session:
        return redirect(url_for("home"))
    else:
        return render_template("login.html")


@app.route("/verifyLogin", methods = ["POST", "GET"])
def verifyLogin():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        existing_user = Users.query.filter_by(name=name, email=email).first()

        if existing_user:
            session["name"] = name
            session["email"] = email
            flash("Logged in Successfully")
            return redirect(url_for("home"))
        else:
            flash("Invalid Credentials!")
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))
    
@app.route("/home")
def home():
    if "name" in session:
        print("Session: ", session)
        print("Hello", session["name"])
        return render_template("home.html")
    else:
        return redirect(url_for("get_in"))

@app.route("/db")
def database():
    return render_template("database.html", values = Users.query.all())

@app.route("/logout")
def logout():
    session.clear()
    print("Session: ", session)
    flash("Logged Out Successfully!")
    return redirect(url_for("get_in"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug = True)