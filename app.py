from flask import Flask, render_template, request, redirect  # from module import Class.

import os
import re
import swim_utils
import hfpy_utils

app = Flask(__name__)

files = os.listdir(swim_utils.FOLDER)
files.remove(".DS_Store")
names = set()
name_dict = {}

for swimmer in files:
        names.add(swim_utils.get_swimmers_data(swimmer)[0])


@app.get("/")
def hello():
    return "Hello from my first web app - cool, isn't it?"  # ANY string.


@app.route('/redirect', methods=['GET','POST'])
def back_to_select_swimmer():
    return redirect("/getswimmers")

@app.post("/chart")
def display_chart():
    (
        name,
        age,
        distance,
        stroke,
        the_times,
        converts,
        the_average,
    ) = swim_utils.get_swimmers_data(request.form["event"])

    the_title = f"{name} (Under {age}) {distance} - {stroke}"
    from_max = max(converts) + 50
    the_converts = [hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts]

    the_data = zip(the_converts, the_times)

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
    )


@app.post("/displayevents")
def get_swimmer_events():
    file_list = []
    for event in files:
        if re.match(request.form["swimmer"], event):
            file_list.append(event)
            name_dict[request.form["swimmer"]] = file_list

        
    return render_template(
        "select_event.html",
        title="Select a event to chart",
        files=sorted(name_dict[request.form["swimmer"]]),
    )


if __name__ == "__main__":
    app.run(debug=True)  # Starts a local (test) webserver, and waits... forever.