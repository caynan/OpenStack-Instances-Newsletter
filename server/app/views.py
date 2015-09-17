from app import app
from script.main import *

@app.route("/instances/delete/<id>")
def instance_delete(id):
    delete_server(id)
    return "Deleted Instance with id: " + id
