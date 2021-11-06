from __future__ import unicode_literals

import atexit
import os
import re
import shlex
import subprocess
from tempfile import mkdtemp
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_session import Session
from werkzeug.exceptions import HTTPException, InternalServerError, default_exceptions
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["secret_key"] = os.getenv("SECRET_KEY")
Session(app)


pwd = os.path.dirname(os.path.abspath(__file__))
formats = []
with open("formats.txt", "r") as file:
    for line in file:
        formats.append(line.strip())


@app.route("/")
def index():
    session.clear()
    p = os.getcwd()
    print(p)
    session["name"] = None
    return render_template("index.html")


@app.route("/done", methods=["GET", "POST"])
def done():
    if request.method == "GET":
        if not session["name"]:
            return redirect(
                url_for("error", text="Please Enter a Valid Link", code=403)
            )
        return render_template("done.html")
    name = session["name"]
    p = os.getcwd()
    return send_from_directory(p, name, as_attachment=True)


@app.route("/waiting", methods=["GET", "POST"])
def waiting():
    if request.method == "GET":
        return render_template("waiting.html")


@app.route("/download", methods=["POST", "GET"])
def download():
    if request.method == "GET":
        return render_template("download.html", formats=formats)
    if not request.form.get("url"):
        error = "Please Enter A Link"
        return render_template("download.html", error=error)
    session["format"] = request.form.get("format")
    session["url"] = request.form.get("url")
    r = request.path
    return render_template("waiting.html", r=r)


@app.route("/convert", methods=["POST", "GET"])
def convert():
    if request.method == "GET":
        return render_template("convert.html", formats=formats)
    files = request.files
    file = request.files["file[0]"]
    format = request.form.get("format")
    file.save(os.path.join(os.getcwd(), file.filename))
    session["file"] = file.filename
    session["format"] = format
    r = request.path
    return "ok"


@app.route("/converter")
def converter():
    file = session["file"]
    file = re.escape(file)
    file = file.replace("'", "\\'")
    file = file.replace('"', '\\"')
    outputfile = file.split(".")[0]
    if session["format"]:
        format = session["format"].lower()
    else:
        format = file.split(".")[1]
    ffmpeg = f"ffmpeg -y -i {file} -strict -2 {outputfile}.{format}"
    session["name"] = f"{session['file'].split('.')[0]}.{format}"
    args = shlex.split(ffmpeg)
    subprocess.call(args)
    return redirect(url_for("done"))


@app.route("/process")
def process():
    url = session["url"]
    format = session["format"].lower()
    try:
        command_line = f"youtube-dl {url}"
        subprocess.call(shlex.split(command_line))
        command_line = f"youtube-dl {url} --get-filename"
        title = subprocess.check_output(
            shlex.split(command_line)).decode("utf-8").strip()
        if format:
            file = title
            file = re.escape(file)
            file = file.replace("'", "\\'")
            file = file.replace('"', '\\"')
            outputfile = file.split(".")[0]
            ffmpeg = f"ffmpeg -y -i {file} -strict -2 {outputfile}.{format} "
            args = shlex.split(ffmpeg)
            subprocess.call(args)
            session["name"] = f"{title.split('.')[0]}.{format}"
        else:
            session["name"] = title
    except:
        args = shlex.split("yotube-dl --rm-cache-dir")
        subprocess.call(args)
        process()
    return title


@app.route("/error")
def error():
    text = request.args["text"]
    code = request.args["code"]
    return apology(text, code)


def delete():
    with app.app_context():
        root = os.listdir(pwd)
        for i in root:
            with open(f"{pwd}/formats.txt") as file:
                for line in file:
                    if i.endswith(line.strip().lower()) or i.endswith(".part"):
                        os.remove(pwd + "/" + i)


atexit.register(delete)


def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("error.html", top=code, bottom=message), code


@app.errorhandler(Exception)
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


@app.route("/update_server", methods=["POST"])
def webhook():
    command_line = "git pull origin main"
    args = shlex.split(command_line)
    subprocess.Popen(args, cwd=pwd)
    return "okay"
