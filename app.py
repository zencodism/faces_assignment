import os
import face_recognition
from flask import Flask, render_template, url_for, redirect, request, flash, send_from_directory
from flask_socketio import SocketIO
from PIL import Image, ImageDraw
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "not super secure, this one"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 6 * 1000 * 1000
socketio = SocketIO(app)

class NoFacesDetected(Exception):
    def __str__(self):
        return "No faces detected in the image"

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    print("Client connected")

@app.route("/uploads/<path:path>")
def uploaded(path):
    return send_from_directory(app.config["UPLOAD_FOLDER"], path)

def validate_upload(request):
    # check if the post request has the file part
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if not file or file.filename == "":
        # browser might supply and empty file in the form submission
        return "No file selected"
    if "image" not in file.mimetype:
        # fairly naive; might want to use magic instead
        return "Not an image file"
    if file.content_length > app.config["MAX_CONTENT_LENGTH"]/2:
        # flask will catch it, but with uglier error screen
        return "File is too big"
    return None

def process_img_upload(file):
    filename = secure_filename(file.filename)
    filename = f"{filename.rsplit('.')[0]}.png"
    img = Image.open(file)
    draw = ImageDraw.Draw(img)
    file.seek(0)
    frimg = face_recognition.load_image_file(file)
    faces = face_recognition.face_locations(frimg)
    if not faces or not len(faces):
        raise NoFacesDetected()
    for face in faces:
        top, right, bottom, left = face
        draw.line(((left, top),
            (right, top),
            (right, bottom),
            (left, bottom),
            (left, top)), fill="blue", width=5)
        # draw.rectangle((left, top, right, bottom), outline="blue")
    if not os.path.isdir(app.config["UPLOAD_FOLDER"]):
        # sanity check, ideally should not happen every time
        os.mkdir(app.config["UPLOAD_FOLDER"])
    img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return url_for("uploaded", path=filename)


@app.route("/image", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        issue = validate_upload(request)
        if issue:
            print("err", issue)
            return redirect(request.url)
        file = request.files["file"]
        try:
            uploaded_url = process_img_upload(file)
            print("UPLOADED", uploaded_url)
        except Exception as e:
            print("Oops", e)
            return redirect(request.url)
        return redirect(uploaded_url)
    return render_template("upload.html")



if __name__ == "__main__":
    socketio.run(app, debug=True)
