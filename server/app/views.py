from app import app

@app.route("/instances/delete/<key>")
def instance_delete(key):
    return "Deleted: " + key
