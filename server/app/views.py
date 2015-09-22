import os
from app import app
from script.main import *

@app.route("/instances/delete/<id>")
def instance_delete(id):
    try:
	delete_server(server_hash=id)
	return '<h3><center>Instance deleted successfully</center></h3>'
    except ValueError:
    	return '<center><h3>Instance not found or already deleted</h3> \
		<p>More information contact the Cloud admin</p></center>'


@app.route("/user/confirm/<id>")
def confirm_action(id):
    os.chdir(os.path.dirname(__file__))
    confirm = open('../../templates/src/confirm.html').read().format(id=id)
    return confirm

