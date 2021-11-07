from __future__ import unicode_literals

import atexit
import os
import re
import shlex
from socket import socket
import subprocess
import json
from threading import Thread
import time

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
socketio = SocketIO(app)


@socketio.on("connect")
def connect():
    print("Client connected")
    socketio.emit("connected", "Connected")


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


def progress_reader(procs, q):
    while True:
        if procs.poll() is not None:
            break  # Break if FFmpeg sun-process is closed

        progress_text = procs.stdout.readline()  # Read line from the pipe

        # Break the loop if progress_text is None (when pipe is closed).
        if progress_text is None:
            break

        progress_text = progress_text.decode(
            "utf-8")  # Convert bytes array to strings

        # Look for "frame=xx"
        if progress_text.startswith("frame="):
            frame = int(progress_text.partition('=')[-1])  # Get the frame number
            q[0] = frame  # Store the last sample


@app.route("/process")
def process():
    url = session["url"]
    format = session["format"].lower()
    try:
        command_line = f"youtube-dl {url}"
        p = subprocess.Popen(shlex.split(command_line), stdout=subprocess.PIPE)
        while True:
            line = p.stdout.readline()
            if not line:
                break
            socketio.emit("update", line.decode("utf-8"))
        command_line = f"youtube-dl {url} --get-filename"
        title = subprocess.check_output(
            shlex.split(command_line)).decode("utf-8").strip()
        if format:
            data = subprocess.run(shlex.split(
                f'ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 -of json {title}'), stdout=subprocess.PIPE).stdout
            # Convert data from JSON string to dictionary
            dict = json.loads(data)
            # Get the total number of frames.
            tot_n_frames = float(dict['streams'][0]['nb_read_packets'])
            file = title
            file = re.escape(file)
            file = file.replace("'", "\\'")
            file = file.replace('"', '\\"')
            outputfile = file.split(".")[0]
            ffmpeg = f"ffmpeg -y -i {file} -strict -2 {outputfile}.{format} "
            process = subprocess.Popen(
                shlex.split(ffmpeg), stdout=subprocess.PIPE)
            q = [0]  # We don't really need to use a Queue - use a list of of size 1
            progress_reader_thread = Thread(target=progress_reader, args=(
                process, q))  # Initialize progress reader thread
            progress_reader_thread.start()  # Start the thread
            while True:
                if process.poll() is not None:
                    break  # Break if FFmpeg sun-process is closed

                time.sleep(1)  # Sleep 1 second (do some work...)

                # Read last element from progress_reader - current encoded frame
                n_frame = q[0]
                progress_percent = (n_frame/tot_n_frames)*100   # Convert to percentage.
                progress_percent = round(int(progress_percent.split(".")[0]))
                socketio.emit("update", progress_percent)
                print(f'Progress [%]: {progress_percent:.2f}')  # Print the progress
            process.stdout.close()          # Close stdin pipe.
            progress_reader_thread.join()   # Join thread
            process.wait()                  # Wait for FFmpeg sub-process to finish
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


if __name__ == "__main__":
    socketio.run(app)
