import getpass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(users):
    # Email from where the messages will be sent.
    email = 'arthurxd11@gmail.com'
    # This gets the password without echoing it on the screen.
    password = getpass.getpass()

    # You need to change here, depending on the email that you use.
    # For example, Gmail and Yahoo have different smtp, 'stmp.gmail.com' and 'smtp.mail.yahoo.com', respectively.
    # You need to know what it is.
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.ehlo()
    smtp.login(email, password)

    for user in sorted(users):
        # If some user owns no server, ignore him.
        if not users[user].has_key('servers'):
           continue

        servers = users[user]['servers']
        destination = users[user]['email']

	messenger = MIMEMultipart('alternative')
        messenger['Subject'] = "HTML"

	html = open('../email_template/base.html').read()
	html = MIMEText(html, 'html')
	messenger.attach(html)	

        smtp.sendmail(email, [destination], messenger.as_string())

    smtp.close()
