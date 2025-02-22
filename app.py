from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory)
from flask_socketio import SocketIO

from operations import process_img_upload, validate_upload

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["SECRET_KEY"] = "not super secure, this one"
app.config["MAX_CONTENT_LENGTH"] = 6 * 1000 * 1000
socketio = SocketIO(app)


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/uploads/<path:path>")
def uploaded(path):
    return send_from_directory(app.config["UPLOAD_FOLDER"], path)


@app.route("/image", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        issue = validate_upload(request, app.config["MAX_CONTENT_LENGTH"] / 2)
        if issue:
            flash(issue, "error")
            return redirect(request.url)
        file = request.files["file"]
        try:
            uploaded_url = process_img_upload(file, app.config["UPLOAD_FOLDER"])
        except Exception as e:
            flash(f"Upload processing error: {e}", "error")
            return redirect(request.url)
        socketio.emit("upload", uploaded_url)
        flash("Upload successful", "success")
    return render_template("upload.html")


@app.route("/faces", methods=["GET"])
def gallery():
    return render_template("gallery.html")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8282, debug=True)
