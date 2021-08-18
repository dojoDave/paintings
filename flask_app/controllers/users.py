from flask_app import app
from flask import render_template,redirect,request,flash,session
from flask_app.models.user import User
from flask_app.models.painting import Painting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():

    if not User.validate_register(request.form):
        return redirect("/")    

    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    User.create_user(data)
    flash(f"{data['email']} has been created! Go ahead and login!")
    return redirect("/")

@app.route("/loginuser", methods=["POST"])
def loginuser():
    
    if not User.validate_login(request.form):
        return redirect("/")    
    
    data = {
        "email":request.form["email"]
    }
    user = User.get_user(data)
    if(user):
        if(bcrypt.check_password_hash(user["password"],request.form["password"])):
            session["user_id"] = user["id"]
            session["email"] = user["email"]
            session["first_name"] = user["first_name"]
            return redirect("/paintings")
        else:
            flash("Incorrect username or password")
            return redirect("/")
    else:
        flash("Incorrect username or password")
        return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")