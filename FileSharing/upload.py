from flask import Blueprint , request , flash , render_template , session , redirect , url_for
import os
import json


send = Blueprint("upload" , __name__)
PATH = os.path.dirname(os.path.abspath("main.py")) + "/"

@send.route("/invia", methods=["POST", "GET"])
def upload():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        file = request.files["uploaded_file"]
        name = request.form["nm"]
        os.chdir(PATH)
        with open("users.json") as f:
            data = json.load(f)
            if name not in data.keys():
                flash("Questo utente non esiste.\nPerfavore assicurati di aver scritto il nome utente correttamente")
            elif file.filename in os.listdir():
                filename = file.filename.copy()
                i = 0
                while file.filename in os.listdir():
                    file.filename = filename + f"({i})"
                    i += 1 
            else:
                os.chdir(PATH + f"database/{name}/") 
                file.save(file.filename)
                flash("Il tuo file è stato inviato con successo!")
    return render_template("upload.html")