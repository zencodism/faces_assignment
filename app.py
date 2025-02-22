from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "not super secure, this one"
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected")


if __name__ == "__main__":
    socketio.run(app, debug=True)
