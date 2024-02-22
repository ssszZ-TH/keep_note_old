#!/usr/bin/env python
import os

from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
mongo_uri = "mongodb://toothless:dragon@mongo:27017/"  # mongo is domain in docker compose
##mongo_uri = os.environ.get("FLASK_MONGO_URI", "mongodb://mongo:27017/keep_notes" )
client = MongoClient(mongo_uri)
db = client["keep_notes"]
notes_collection = db["notes"]


## read 
@app.route("/")
def list_notes():
    notes = notes_collection.find()
    ##test root page######################################################## pass
    #return "demo"
    #########################################################################
    # print(type(notes))
    # print(notes)
    return render_template("list.html", notes=notes)

## create
@app.route("/new", methods=["GET", "POST"])
def new_note():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        note = {"title": title, "content": content}
        notes_collection.insert_one(note)
        return redirect("/")
    return render_template("new.html")

## update
@app.route("/note/<note_id>", methods=["GET", "POST"])
def view_note(note_id):
    note = notes_collection.find_one({"_id": ObjectId(note_id)})
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        note["title"] = title
        note["content"] = content
        notes_collection.update_one({"_id": ObjectId(note_id)}, {"$set": note})
        return redirect("/")
    return render_template("edit.html", note=note)

## delete
@app.route("/delete/<note_id>")
def delete_note(note_id):
    notes_collection.delete_one({"_id": ObjectId(note_id)})
    return redirect("/")





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9091), debug=True)

