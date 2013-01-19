#CARRIER SMS GATEWAY
ATT     = "@txt.att.net"
SPRINT  = "@messaging.sprintpcs.com"
TMOBILE = "@tmomail.net"
VERIZON = "@vtext.com"

#GMAIL Setting (IMPORTANT)
GMAIL_USER = "user@gmail.com"
GMAIL_PWD  = "pwd"

#Contact Setting
EMAIL = "test@gmail.com"
USE_EMAIL = True
PHONE = "123456789"
USE_PHONE = True
CARRIER = "TMOBILE"

#Clases to Alert 
#sec_num: all, 1b (all checks for lecture)
#alert rule: open (enroll < cap) This option is useless rightnow
#once alerted, the rule will be removed from application (in the application memory but config file is unchanged)

#-------EXAMPLE  (follow the format)-------
#
# CLASSES_ALERT.append({"term" : "13W",
#                   "major" : "COM+SCI",
#                    "course" : "0112++++",
#                   "lec_num" : 1,
#                    "sec_num" : "1A",
#                    "alert" : "open"
#                })
#
#-------------------------------------------
CHECK_EVERY_SEC = 15
CLASSES_ALERT = []
CLASSES_ALERT.append({"term" : "13W",
                "major" : "COM+SCI",
                "course" : "0112++++",
                "lec_num" : 1,
                "sec_num" : "1A",
                "alert" : "open"
                })
CLASSES_ALERT.append({"term" : "13W",
                "major" : "COM+SCI",
                "course" : "0143++++",
                "lec_num" : 1,
                "sec_num" : "1C",
                "alert" : "open"
                })

#add more by appending to CLASSES using the same style (all fields must be filled up)
