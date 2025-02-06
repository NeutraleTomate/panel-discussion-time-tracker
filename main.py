from engineio.async_drivers import gevent
from flask import Flask, render_template
import flask_socketio as io
import flask_apscheduler

import timetracker

app = Flask(__name__)
socketio = io.SocketIO(app)

speakers = [
    {"party": "CDU",
     "name": "Dr. Markus Reichel",
     "color": "#000000"},

    {"party": "SPD",
     "name": "Fabian Funke",
     "color": "#E3000F"},

    {"party": "B90/Grüne",
     "name": "Bernhard Herrmann",
     "color": "#46962b"},

    {"party": "Die Linke",
     "name": "Nina Treu",
     "color": "#bc3373"},

    {"party": "FDP",
     "name": "Toralf Einsle",
     "color": "#ffed00"}
]

timetracker = timetracker.TimeTracker(speakers)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/presentation')
def presentation():
    return render_template("presentation.html")


@app.route('/controls')
def controls():
    return render_template("controls.html", speakers=timetracker.names(), colors=timetracker.colors())


@socketio.on('start')
def start(data):
    timetracker.start(data["name"])


@socketio.on('stop')
def stop(data):
    timetracker.stop(data["name"])

@socketio.on('update')
def send_update(d):
    to=d["sid"]
    
    names = timetracker.names()
    times = timetracker.times()
    times_total = timetracker.times_total()
    colors = timetracker.colors()
    active = timetracker.active()
    data = {
        "labels": names,
        "data": times_total,
        "colors": colors,
    }
    with app.test_request_context('/presentation'):
        socketio.emit("update_pres", data,to=to)
    data2= {
        "labels": names,
        "times": times,

        "colors": colors,
        "active":active
    }

    with app.test_request_context('/controls'):
        socketio.emit("update_ctrl", data2,to=to)


if __name__ == "__main__":
    print("start")
    socketio.run(app, host="127.0.0.1")
    
