from app import app
from script.main import *

@app.route("/instances/delete/<id>")
def instance_delete(id):
    try:
	delete_server(server_hash=id)
	return "<h1>Instance deleted successfully</h1>"
    except ValueError:
    	raise NotImplementedError


@app.route("/user/confirm/<id>")
def confirm_action(id):
    raise NotImplementedError

