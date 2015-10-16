import os
from server import APP
from flask.ext.api import status
from script.main import delete_server

@APP.route("/instances/delete/<id>")
def instance_delete(id):
    try:
	delete_server(server_hash=id)
	return '<h3><center>Instance deleted successfully</center></h3>'
    except ValueError:
    	return '<center><h3>Instance not found or already deleted</h3> \
		<p>More information contact the Cloud admin</p></center>'


@APP.route("/user/confirm/<id>")
def confirm_action(id):
    os.chdir(os.path.dirname(__file__))
    url = 'http://haproxy_ip:80/instances/delete/' + id

    confirm = open('../../templates/src/confirm.html').read().format(url=url)
    return confirm

@APP.route("/")
def monitor():
    return status.HTTP_200_OK
