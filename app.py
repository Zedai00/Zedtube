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

app = Flask(__name__)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["secret_key"] = "b'^\xe5\xcb\xac\xd0`\x1co\x82\x97J\x8a\x81?\x00\x1a'"
Session(app)

pwd = os.path.dirname(os.path.abspath(__file__))
formats = []
with open("formats.txt", "r") as file:
    for line in file:
        formats.append(line.strip())


@app.route("/")
def index():
    session.clear()
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
    path = os.getcwd()
    return send_from_directory(path, name, as_attachment=True)


@app.route("/download", methods=["POST", "GET"])
def download():
    if request.method == "GET":
        return render_template("download.html", formats=formats)
    if not request.form.get("url"):
        error = "Please Enter A Link"
        return render_template("download.html", error=error)
    session["url"] = request.form.get("url")
    r = request.path
    return render_template("waiting.html", r=r)


@app.route("/convert", methods=["POST", "GET"])
def convert():
    if request.method == "GET":
        return render_template("convert.html", formats=formats)
    if not request.files["file"]:
        error = "Please Choose A File To Upload"
        return render_template("convert.html", error=error)
    file = request.files["file"]
    format = request.form.get("format")
    file.save(os.path.join(os.getcwd(), file.filename))
    session["file"] = file.filename
    session["format"] = format
    r = request.path
    return render_template("waiting.html", r=r)


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
    ffmpeg = f"ffmpeg -i {file} -preset ultrafast -codec copy {outputfile}.{format}"
    session["name"] = f"{session['file'].split('.')[0]}.{format}"
    args = shlex.split(ffmpeg)
    subprocess.call(args)
    return redirect(url_for("done"))


@app.route("/process")
def process():
    url = session["url"]
    format = request.form.get("format").lower()
    if format:
        command_line = f"youtube-dl {url} --merge-output-format {format}"
        command_line = re.escape(command_line)
        command_line = command_line.replace("'", "\\'")
        command_line = command_line.replace('"', '\\"')
        subprocess.call(shlex.split(command_line))
        command_line = f"youtube-dl {url} --get-filename -merge-output-format {format} --skip-download"
        command_line = re.escape(command_line)
        command_line = command_line.replace("'", "\\'")
        command_line = command_line.replace('"', '\\"')
        title = subprocess.check_output(shlex.split(command_line)).decode("utf-8")
    else:
        command_line = f"youtube-dl {url}"
        command_line = re.escape(command_line)
        command_line = command_line.replace("'", "\\'")
        command_line = command_line.replace('"', '\\"')
        subprocess.call(shlex.split(command_line))
        command_line = f"youtube-dl {url} --get-filename"
        command_line = re.escape(command_line)
        command_line = command_line.replace("'", "\\'")
        command_line = command_line.replace('"', '\\"')
        title = subprocess.check_output(shlex.split(command_line)).decode("utf-8")
    session["name"] = title
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
    os.system("git pull origin main --no-edit")
    return "okay"
