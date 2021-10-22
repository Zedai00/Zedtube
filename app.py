from __future__ import unicode_literals
import os
import redis
from tempfile import mkdtemp

import youtube_dl
from flask import (Flask, render_template, request, send_file,
                   send_from_directory, session)
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_TYPE"] = "redis"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_REDIS"] = redis.from_url(os.environ.get("REDIS_SESSION"))
Session(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST", "GET"])
def download():
    if request.method == "GET":
        return render_template("download.html")
    else:
        session["url"] = request.form.get("url")
        return render_template("waiting.html")


@app.route("/process")
def process():
    url = session["url"]
    ydl_opts = {"cachedir": "False", "ignoreerrors": "True"}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(
            [
                url,
            ]
        )
        result = ydl.extract_info("{}".format(url))
        name = ydl.prepare_filename(result)
        session["name"] = name
        return name


@app.route("/done", methods=["GET", "POST"])
def done():
    if request.method == "GET":
        return render_template("done.html")
    name = session["name"]
    return send_from_directory(app.root_path, name, as_attachment=True)
