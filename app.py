import os
from flask import Flask, render_template, url_for, redirect, request, flash, send_from_directory
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "not super secure, this one"
app.config["UPLOAD_FOLDER"] = "uploads"
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected")

@app.route("/uploads/<path:path>")
def uploaded(path):
    return send_from_directory(app.config["UPLOAD_FOLDER"], path)


@app.route("/image", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if not file or file.filename == "":
            # browser might supply and empty file in the form submission
            flash("No file selected")
            return redirect(request.url)
        if "image" not in file.mimetype:
            # fairly naive; might want to use magic instead
            flash("Not an image file")
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return redirect(url_for('uploaded', path=filename))
    return render_template("upload.html")


if __name__ == "__main__":
    socketio.run(app, debug=True)
