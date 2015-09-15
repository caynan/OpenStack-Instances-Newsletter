# OpenStack Instances Newsletter


## Description
A small script to send all users of the OpenStack cloud an email about their
account instances, informing that of inactivity and are giving the option to delete
their Instances from their email.

## Installation
1. clone the repo
  ```
  $ git clone https://github.com/caynan/OpenStack-Instances-Newsletter.git
  ```  
2. getting into ```src``` and change the environment variables inside
```openrc.sh``` to the ones that match your cloud, save and run the script.
  ```
  $ ./openrc.sh
  ```
3. run the app!!
  ```
  $ python main.py
  ```

## Troubleshooting

### If you're running this using **Gmail**

#####Step 1: Ensure your password is correct

#####Step 2: Enable Less Secure Apps
    Google is not allowing you to log in via smtplib because it has flagged this sort of login as 'less secure', in order to login, follow this:
        1. Login to Gmail in your browser
        2. Navigate to this link: https://www.google.com/settings/security/lesssecureapps
        3. Select 'Enable'

After enabling 'less secure apps' you'll have to wait some minutes, go for a coffee, relax... and continue.

#####Step 3: Disable CAPTCHA for clients
    1. Login to Gmail in your browser
    2. Navigate to this link: http://www.google.com/accounts/DisplayUnlockCaptcha
    3. Click the continue button, and you will see the message: 'Account access enabled. Please try signing in to your Google account again from your new device or application.'

Run the script again, your login attempt should be successful.
