from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "kIhas@1jnmas}a}[asd]!!|aq1h28856565562"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    task = db.Column(db.String(10000))
    history = db.Column(db.String(10000000))

    def __init__(self, name, email, task, history):
        self.name = name
        self.email = email
        self.task = task
        self.history = history

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
            new_user = Users(name, email, task = "", history="")
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
    
@app.route("/record")
def record():
    return render_template("record.html")
    
@app.route("/add_task", methods = ["POST", "GET"])
def add_task():
    if request.method == "POST":
        task = request.form["task"]
        print(task)
        if len(task)>0:
            #adding task:
            user = Users.query.filter_by(name=session["name"], email=session["email"]).first()
            if user:
                user.task = (user.task or "") + task + ","
                user.history = user.task
            try:
                db.session.commit()
                print("Task Added Successfully to DataBase")
                print(jsonify(success = True))
                return jsonify(success=True)
                # return redirect(url_for("get_tasks"))
            except:
                print("Issue in adding a task")
                print(jsonify(success=False, error = "Issue in adding your task!"))
                return jsonify(success=False, error = "Issue in adding your task!")
            
        else:
            print(jsonify(success=False, error = "Can't add blank task!"))
            return jsonify(success=False, error = "Can't add blank task!")
            # return redirect(url_for("get_tasks"))

    else:
        pass

@app.route("/get_tasks")
def get_tasks():
    tasks = [t[0] for t in db.session.query(Users.task).filter_by(name = session["name"], email = session["email"]).all()]
    
    if len(tasks) == 0:
        return render_template("partials/task_list.html", tasks = "")
    else:
        task_array = [task.strip() for task in tasks[0].split(",")]
        print(task_array)
        return render_template("partials/task_list.html", tasks = task_array)
    
@app.route('/delete/<task>')
def delete(task):
    print(task)
    user = Users.query.filter_by(name=session["name"], email=session["email"]).first()
    if user:
        print(user.task)

        user.task = user.task.replace(task+',', "")
        db.session.commit()
        print("Task Removed Successfully")
        return jsonify(success = True)
    else:
        return jsonify(success = False, error = "Task not found"), 404
    

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