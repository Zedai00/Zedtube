from __future__ import unicode_literals
import os
from werkzeug.utils import send_from_directory
import youtube_dl
from flask import Flask, redirect, render_template, request, send_file,send_from_directory, safe_join, abort
import ffmpeg

app = Flask(__name__)

@app.route("/")
def index():
        return render_template("index.html")

@app.route("/download", methods=["POST", "GET"])
def download():
    if request.method == "GET":
        return render_template("download.html")
    else:
        url = request.form.get("url")
        ydl_opts = {
            "cachedir": "False",
            "ignoreerrors": "True"
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url,])
            result = ydl.extract_info("{}".format(url))
            name = ydl.prepare_filename(result)

            name = os.system("ffmpeg -i " + name + "-preset ultrafast test.mkv")
            return send_from_directory(app.root_path, "test.mkv", as_attachment=True)
