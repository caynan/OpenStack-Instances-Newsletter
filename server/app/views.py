from app import app
from script.main import *

@app.route("/instances/delete/<id>")
def instance_delete(id):
    delete_server(server_hash=id)
    return "Instance deleted successfully"
