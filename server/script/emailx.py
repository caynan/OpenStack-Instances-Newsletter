import os
import getpass
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ADMIN_EMAIL = 'diego_adolff@hotmail.com'

def send_email(users):
    """ Send email to cloud users informing about their instances. """

    # Email from where the messages will be sent.
    email = 'diegoado@gmail.com'
    # This gets the password without echoing it on the screen.
    password = getpass.getpass()

    # You need to change here, depending on the email that you use.
    # For example, Gmail and Yahoo have different smtp, 'stmp.gmail.com' and 'smtp.mail.yahoo.com', respectively.
    # You need to know what it is.
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.ehlo()
    smtp.login(email, password)

    # Iterate through cloud users and send emails.
    for user in sorted(users):
        # If some user owns no server, ignore him.
        if not users[user].has_key('servers'):
           continue

        servers = users[user]['servers']
        destination = users[user]['email']

	messenger = get_messenger(user, servers)
        smtp.sendmail(email, [destination], messenger)

    smtp.close()


def get_messenger(user, servers):
    """ Construct the email content with user's instances information. 

    Keyword arguments:
    user -- user who will receive the email
    servers -- list of instances owned by the user
    """
    os.chdir(os.path.dirname(__file__))

    messenger = MIMEMultipart('alternative')
    messenger['Subject'] = 'Instances Newletter'

    instances = ''
    instance_model = open('../../templates/models/instances.html').read()
    for server in sorted(servers, key = servers.get):
    	instance = instance_model
    	instance = instance.format(instance_name = server,
    			           cpu = servers[server]['cpu'],
    			           ram = servers[server]['ram'],
    			           date = servers[server]['created'],
    			           status = servers[server]['status'],
                                   url = get_url(servers[server]['hash']))

        instances += instance

    base = open('../../templates/models/base.html').read().format(user_name = user,
								  instances = instances)
    html = MIMEText(base, 'html')
    messenger.attach(html)

    return messenger.as_string()

def get_url(server_hash):
    return "http://10.4.2.207:9898/user/confirm/{id}".format(id = server_hash)

