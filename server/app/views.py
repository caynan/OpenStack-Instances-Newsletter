from app import app
from script import main

@app.route("/instances/delete/<key>")
def instance_delete(key):
    return "Deleted: " + key
