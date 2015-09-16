from app import app
from script import main as terminator

@app.route("/instances/delete/<id>")
def instance_delete(id):
    terminator.delete_server(id)
    return "Deleted Instance with id: " + id
