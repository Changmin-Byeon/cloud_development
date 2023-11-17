from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
)  # from module import Class.

import os
import re
import swim_utils
import hfpy_utils

app = Flask(__name__)
app.secret_key = "cloud development ca"

files = os.listdir(swim_utils.FOLDER)
files.remove(".DS_Store")
names = set()
name_age = {}
show_events = {}

for swimmer in files:
    names.add(swim_utils.get_swimmers_data(swimmer)[0])
    name_age[swim_utils.get_swimmers_data(swimmer)[0]] = swim_utils.get_swimmers_data(
        swimmer
    )[1]


@app.get("/")
def hello():
    return 'Hello from my first <a href="/getswimmers">web app</a> - cool, isn\'t it?'  # ANY string.


@app.route("/redirect", methods=["GET", "POST"])
def back_to_select_swimmer():
    session.pop("swimmer", None)
    return redirect("/getswimmers")


@app.post("/chart")
def display_chart():
    filename = (
        session["swimmer"]
        + "-"
        + name_age[session["swimmer"]]
        + "-"
        + request.form["event"].split(" ")[0]
        + "-"
        + request.form["event"].split(" ")[1]
        + ".txt"
    )

    (
        name,
        age,
        distance,
        stroke,
        the_times,
        converts,
        the_average,
    ) = swim_utils.get_swimmers_data(filename)

    the_title = f"{name} (Under {age}) {distance} - {stroke}"
    from_max = max(converts) + 50
    the_converts = [hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts]

    the_data = zip(reversed(the_converts), reversed(the_times))

    return render_template(
        "chart.html",
        title=the_title,
        average=the_average,
        converts=the_converts,
        times=the_times,
        data=the_data,
    )


@app.get("/getswimmers")
def get_swimmers_name():
    return render_template(
        "select_swimmer.html",
        title="Select a swimmer to chart",
        data=sorted(names),
        data2=name_age,
    )


@app.post("/displayevents")
def get_swimmer_events():
    session["swimmer"] = request.form["swimmer"]
    event_list = []
    for file in files:
        if re.match(request.form["swimmer"], file):
            event = file.split("-")[2] + " " + file.split("-")[3].removesuffix(".txt")
            event_list.append(event)
            show_events[request.form["swimmer"]] = event_list

    return render_template(
        "select_event.html",
        title="Select a event to chart",
        files=sorted(show_events[request.form["swimmer"]]),
    )


if __name__ == "__main__":
    app.run(debug=True)  # Starts a local (test) webserver, and waits... forever.
