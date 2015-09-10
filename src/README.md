# PLEASE READ

This script assums that the environment variables are setted. If they're not, you should set them at 'openrc.sh' file.
In order to send emails, you'll need to change 'emailx.py'. Method documentation will guide you.

If 'SMTPAuthenticationError' exception was thrown when you attempted to login to Gmail via Python's smtp library, follow this steps:
	Step 1: Ensure your password is correct
	
	Step 2: Enable Less Secure Apps
		Google is not allowing you to log in via smtplib because it has flagged this sort of login as 'less secure', in order to login, follow this:
			- Login to Gmail in your browser
			- Navigate to this link: https://www.google.com/settings/security/lesssecureapps
			- Select 'Enable'

	After enabling 'less secure apps' you'll have to wait some minutes, go for a coffee, relax... and continue. 
	
	Step 3: Disable CAPTCHA for clients
		1. Login to Gmail in your browser
		2. Navigate to this link: http://www.google.com/accounts/DisplayUnlockCaptcha
		3. Click the continue button, and you will see the message: 'Account access enabled. Please try signing in to your Google account again from your new device or application.'
	
	Run the script again, your login attempt should be successful.
