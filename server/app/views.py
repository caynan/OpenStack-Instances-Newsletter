from app import app
from script.main import *

@app.route("/instances/delete/<id>")
def instance_delete(id):
    try:
	delete_server(server_hash=id)
	return "<h1>Instance deleted successfully</h1>"
    except ValueError:
    	return "<h1>Instance deleted successfully</h1>"


@app.route("/instances/confirm/<id>")
def confirm_action(hash):
    pass

