from flask import Blueprint , request , send_file , render_template , session, redirect , url_for , flash
import os


receive = Blueprint("download" ,__name__)
PATH = os.path.dirname(os.path.abspath("main.py")) + "/"

@receive.route("/ricevuti" , methods=["GET" , "POST"])
def download():
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    os.chdir(PATH + f"database/{user}")
    if request.method == "POST":
        file_name = request.form["file_name"]
        return send_file("database/" + file_name)
    files = os.listdir()
    if not len(files) > 0:
        flash("Non hai ricevuto nessun file ci dispiace :-( !")
        return redirect(url_for("home"))
    return render_template("download.html" , files= os.listdir())