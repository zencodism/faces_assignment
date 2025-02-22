import os

import face_recognition
from flask import url_for
from PIL import Image, ImageDraw
from werkzeug.utils import secure_filename


class NoFacesDetected(Exception):
    def __str__(self):
        return "No faces detected in the image"


def validate_upload(request, content_limit: int):
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
    if file.content_length > content_limit / 2:
        # flask will catch it, but with uglier error screen
        return "File is too big"
    return None


def process_img_upload(file, upload_folder: str):
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
        draw.line(
            ((left, top), (right, top), (right, bottom), (left, bottom), (left, top)),
            fill="blue",
            width=5,
        )
        # draw.rectangle((left, top, right, bottom), outline="blue")
    if not os.path.isdir(upload_folder):
        # sanity check, ideally should not happen every time
        os.mkdir(upload_folder)
    img.save(os.path.join(upload_folder, filename))
    return url_for("uploaded", path=filename)
