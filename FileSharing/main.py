from flask import Flask , render_template , session , redirect , url_for , request , flash
from upload import send
from download import receive
from datetime import timedelta
from werkzeug.security import generate_password_hash , check_password_hash
import os
import json


PATH = os.path.dirname(os.path.abspath("main.py")) + "/"


app = Flask(__name__)
app.secret_key = "sacbuh-7novba-Fefdat"
app.register_blueprint(send , url_prefix="")
app.register_blueprint(receive , url_prefix="")
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/" , methods=["GET" , "POST"])
def home():
    if "user" in session.keys():
        if request.method == "POST":
            password = generate_password_hash(request.form["pw"])
            os.chdir(PATH)
            f = open("users.json" , "r")
            data = json.load(f)
            f.close()
            data.update({session["user"]:password})
            f = open("users.json" , "w")
            f.seek(0)
            f.write(json.dumps(data))
            f.close()
            flash("La tua password è stata cambiata")
        return render_template("index.html", user=session["user"])
    else:
        return redirect(url_for("login"))


@app.route("/accedi", methods=["GET" , "POST"])
def login():
    if request.method == "POST":
        password = request.form["pw"]
        name = request.form["nm"]
        os.chdir(PATH)
        with open("users.json") as f:
            users = json.load(f)
            if name not in users.keys():
                flash("Questo utente non è registrato. Registralo prima di accedere!")
            elif not check_password_hash(users[name] , password):
                flash("Nome utente e/o password errato/i.\nSe non ricordi la password e vuoi reimpostarla mi dispiace non puoi.\nQuesto servizio non è così avanzato.")
            elif check_password_hash(users[name] , password):
                session.permanent = True
                session["user"] = name
                return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/registrati" , methods=["GET" , "POST"])
def register():
    if request.method == "POST":
        name = request.form["nm"]
        password = generate_password_hash(request.form["pw"])
        os.chdir(PATH)
        f = open("users.json" , "r")
        data = json.load(f)
        f.close()
        if name in data.keys():
            flash("Questo utente è già registrato.")
        else:
            data.update({name:password})
            f = open("users.json" , "w")
            f.seek(0)
            f.write(json.dumps(data))
            f.close()
            session["user"] = name
            if not os.path.exists(PATH + f"database/{name}"):
                os.chdir(PATH + "database/")
                os.mkdir(f"{name}")
                pass
            else:
                os.chdir(PATH +  f"database/{name}")
                for file in os.listdir():
                    os.remove(file)
            return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/esci")
def logout():
    del session["user"]
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0" , port="4000")
