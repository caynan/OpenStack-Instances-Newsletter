import getpass
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(users):
    # Email from where the messages will be sent.
    email = 'your_email@email.com'
    # This gets the password without echoing it on the screen.
    password = getpass.getpass()

    # You need to change here, depending on the email that you use.
    # For example, Gmail and Yahoo have different smtp, 'stmp.gmail.com' and 'smtp.mail.yahoo.com', respectively.
    # You need to know what it is.
    smtp = smtplib.SMTP_SSL('smtp.your_mail_server.com', 465)
    smtp.ehlo()
    smtp.login(email, password)

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
    messenger = MIMEMultipart('alternative')
    messenger['Subject'] = 'Instances Newletter'

    instances = ''
    instance_model = open('../email_template/models/instances.html').read()
    for server in sorted(servers, key = servers.get):
	instance = instance_model
	instance = instance.format(instance_name = server,
			           cpu = servers[server]['cpu'],
			           ram = servers[server]['ram'],
			           date = servers[server]['created'],
			           status = servers[server]['status'])

        instances += instance

    base = open('../email_template/models/base.html').read().format(user_name = user,
								    instances = instances)
    html = MIMEText(base, 'html')
    messenger.attach(html)

    return messenger.as_string()
