import getpass
import smtplib

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

        messenger = "\r\n".join(["From: %s" % email, "To: %s" % destination, "Subject: Just a message", "", "Why, oh why"])
        smtp.sendmail(email, [destination], messenger)

    smtp.close()
