from __future__ import unicode_literals
import os
import io
import redis
from tempfile import mkdtemp
import youtube_dl
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from flask import (Flask, render_template, request, send_file,
                   send_from_directory, session, flash, redirect, url_for)
from flask_session import Session
import atexit

app = Flask(__name__)

app.config["SESSION_TYPE"] = "redis"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_REDIS"] = redis.from_url(os.environ.get("REDIS_SESSION"))
Session(app)


@app.route("/")
def index():
    session.clear()
    session['name'] = None
    return render_template("index.html")


@app.route("/download", methods=["POST", "GET"])
def download():
    if request.method == "GET":
        return render_template("download.html")
    else:
        if not request.form.get('url'):
            error = 'Please Enter A Link'
            return render_template('download.html', error=error)
        session["url"] = request.form.get("url")
        return render_template("waiting.html")


@app.route("/process")
def process():
    url = session["url"]
    ydl_opts = {"cachedir": "False"}
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    ydl.download(
        [
            url,
        ]
    )
    result = ydl.extract_info("{}".format(url))
    name = ydl.prepare_filename(result)
    session["name"] = name

@app.route("/error")
def error():
    text = request.args['text']
    code = request.args['code']
    return apology(text, code)

def delete():
    with app.app_context():
        root = os.listdir(app.root_path)
        for i in root:
            if i.endswith(".mp4"):
                os.remove(app.root_path+'/'+i)


atexit.register(delete)


@app.route("/done", methods=["GET", "POST"])
def done():
    if request.method == "GET":
        if not session['name']:
            return redirect(url_for('error', text='Please Enter a Valid Link', code=403))
        return render_template("done.html")
    name = session["name"]
    # mime = mimetypes.guess_type(name)
    # file_path = app.root_path+'/'+name
    # return_data = io.BytesIO()
    # with open(file_path, 'rb') as fo:
    #     return_data.write(fo.read())
    # # (after writing, cursor will be at last byte, so move it to start)
    # return_data.seek(0)

    # os.remove(file_path)

    # return send_file(return_data, mimetype=mime[0],
    #                  attachment_filename=name, as_attachment=True)

    return send_from_directory(app.root_path, name, as_attachment=True)


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
