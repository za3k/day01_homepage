#!/bin/python3
import flask, flask_login
from itertools import *
from collections import defaultdict
from datetime import datetime
from base import app,load_info,ajax,DBDict

# -- Info for every Hack-A-Day project --
load_info({
    "project_name": "Hack-A-Homepage",
    "source_url": "https://github.com/za3k/day01_homepage",
    "subdir": "/hackaday/homepage"
})

# -- Routes specific to this Hack-A-Day project --
people = DBDict("person")

def text(x): return x
def link(l="{}",t="{}"): return lambda x: "<a href=\"{}\">{}</a>".format(l.format(x), t.format(x))
FIELDS = {
    "input": [
        ("Nickname", "XXCoolFroodXX", text),
        ("Full_Name", "John Smith", text),
        ("Email", "jsmith@gmail.com", link("mailto:{}")),
        ("Location", "austin, texas", text),
        ("Phone_Number", "(+1) 555-555-5555", link("tel:{}")),
        #("Facebook_ID", 
        #"Steam_ID": None,
        #"Discord": None,
        #"Snapchat": None,
        #"Instagram": None,
        ("Github", "codername", link("http://github.com/{}", "github.com/{}")),
        ("Twitter", "abird (no @)", link("http://twitter.com/{}", "@{}")),
        ("IRC", "irc_username", text),
        ("Link_1", "", link()),
        ("Link_2", "", link()),
        ("Link_3", "", link()),
        ("Link_4", "", link()),
        ("Link_5", "", link()),
    ],
    "textarea": [
        ("About_Me", "describe yourself with words", text),
        #("Custom_HTML", "you can insert some custom HTML here", html),
    ]
}

def combine(user_id):
    result = {}
    person = people.get(user_id, defaultdict(str))
    for type_, fields in FIELDS.items():
        r = []
        for text_field, d, formatter in fields:
            r.append({
                "key": text_field,
                "display": text_field.replace("_", " "),
                "example": d,
                "value": person[text_field],
                "displayValue": formatter(person[text_field]),
            })
        result[type_] = r
    return result

@app.route("/")
def index():
    user_ids = sorted(islice(people, 0, 10))
    return flask.render_template('index.html', user_ids=user_ids)

@app.route("/edit", methods=["GET", "POST"])
@flask_login.login_required
def edit():
    user_id = flask_login.current_user.id
    if flask.request.method == "POST":
        f = flask.request.form
        print(f)
        people[user_id] = {k:v for k,v in f.items()}
    print(people.get(user_id))
    print(combine(user_id))
    return flask.render_template('edit.html', fields=combine(user_id))

@app.route("/v/<user_id>")
def view(user_id):
    return flask.render_template('view.html', fields=combine(user_id))
