from engineio.async_drivers import gevent
from flask import Flask, render_template
import flask_socketio as io
import yaml

import timetracker

app = Flask(__name__)
socketio = io.SocketIO(app)

try:
    with open("speakers.yaml", "r") as file:
        speakers = yaml.safe_load(file)["speakers"]
except:
    speakers = None


if speakers is not None:
    timetracker = timetracker.TimeTracker(speakers)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/presentation')
def presentation():
    return render_template("presentation.html")


@app.route('/controls')
def controls():
    return render_template("controls.html", speakers=timetracker.labels(), colors=timetracker.colors())


@app.route('/delete')
def delete():
    return render_template("delete.html")


@socketio.on('start')
def start(data):
    timetracker.start(data["name"])


@socketio.on('stop')
def stop(data):
    timetracker.stop(data["name"])


@socketio.on('update')
def send_update(d):
    to = d["sid"]

    names = timetracker.names()
    labels = timetracker.labels()
    times = timetracker.times()
    times_total = timetracker.times_total()
    colors = timetracker.colors()
    active = timetracker.active()
    data = {
        "labels": labels,
        "data": times_total,
        "colors": colors,
    }
    with app.test_request_context('/presentation'):
        socketio.emit("update_pres", data, to=to)
    data2 = {
        "labels": labels,
        "names": names,
        "times": times,
        "times_total": times_total,
        "colors": colors,
        "active": active
    }

    with app.test_request_context('/controls'):
        socketio.emit("update_ctrl", data2, to=to)


@socketio.on('delete')
def delete(data):
    timetracker.delete(data["identifier"])


if __name__ == "__main__":
    if speakers is None:
        print("Error: could not read any speakers from file speakers.yaml")
        print("You can use yamlchecker.com or similar tools to check the contents of your yaml file")
    else:
        print("Running on 127.0.0.1:5000")
        socketio.run(app, host="127.0.0.1", port=5000)
