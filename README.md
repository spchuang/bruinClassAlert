Bruin Class Alert
================
A very hand app that allows UCLA students to track down classes and be alerted when they are open!

Why this?
------------
Have you ever had trouble enrolling in the classes you want at UCLA? The level of frustration that this could lead to is tremendous. Sometimes, if we are lucky we could get in but most of the time, it's impossible. Having to check the registrar website repeatedly everyday is annoying. Don't you wish there's an app out there that can do this task repeatedly every 20 seconds? I know there are websites like course ninja and classscanner (which are great applications) that do similar things. However, the problem with those applications is that they are unable to constantly check the enrollment status due to limited server loads. This light-weight python script allows you to  add any any number of classes you want and be alerted in text or email.



Installation
------------
1.  Clone or download the repo

2.  Set up the correct contact (email/phone) information in setting.py

3.  Add the classes you want to target in setting.py (make sure to follow the template format)

4.  run python bruinClassAlert.py


Settings
------------
1.  Gmail Setting: This application uses simple python SMTP server to send message to your email and phone. We need to use a working GMail for the outgoing SMTP server and it requires some authorization of the account.

    ```python
    GMAIL_USER = "user@gmail.com"
    GMAIL_PWD  = "pwd"

    ```
2.  Contact Settings: Setting for methods and customization of your contact information
    
    ```python
    EMAIL = "test@gmail.com"
    USE_EMAIL = True
    PHONE = "123456789"
    USE_PHONE = True
    CARRIER = "TMOBILE"

    ```
    Note: Carrier name must follow the definition in the setting file: 
    
    ```python
    ATT     = "@txt.att.net"
    SPRINT  = "@messaging.sprintpcs.com"
    TMOBILE = "@tmomail.net"
    VERIZON = "@vtext.com"
    ```

3.  Add the classes you want to target: Specify the term, major, course id of your target course. This information could be found from the url parameters on the registrar website. Also specify the lecture number (in integer) and the section number (in string). Section number could also be "all", which tells the program to notify open spot for the entire lecture.

    
    ```python
    CLASSES_ALERT.append({"term" : "13W",
                "major" : "COM+SCI",
                "course" : "0112++++",
                "lec_num" : 1,
                "sec_num" : "1A",
                })
    ```

