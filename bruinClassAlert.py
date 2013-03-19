#-----------------------------------------------------------------------------
# Name: bruinClassAlert.py
# Purpose: alerts students for open schedules
#
# Author: <Samping Chuang>
# Email : sampingchuang@gmail.com
#
# Created: 2013/01/18
# Copyright: (c) 2013
# Licence: 
#-----------------------------------------------------------------------------
import sys
import getBruinSchedule
import json
import smtplib
import time
from email.mime.text import MIMEText
from time import gmtime, strftime

#opening config file
config = {}
execfile("setting.py", config) 

def sendAlert(text):
    if config['USE_EMAIL']:
        sendMsg(config['EMAIL'], text)
    if config['USE_PHONE']:
        sendMsg(config['PHONE'] + config[config['CARRIER']], text)

#sending an email message
def sendMsg(to, text):
    # Send the message via our own SMTP server, but don't include the
    # envelope headers
    gmail_user = config['GMAIL_USER']
    gmail_pwd = config['GMAIL_PWD']
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    print "sending alert..."
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n'
    msg = header + '\n This is Bruin Class Alert \n\n' + text
    print msg
    #send mail!
    print "\n`"
    smtpserver.sendmail(gmail_user, to, msg)
    smtpserver.close()


if __name__ == '__main__':

    while config['CLASSES_ALERT']:
        print ("checking...")
        for C_ALERTS in config['CLASSES_ALERT']:
            try:
                 c_info = getBruinSchedule.get_class_info(C_ALERTS['term'], \
                                                         C_ALERTS['major'], \
                                                         C_ALERTS['course'])
            except:
		print("Error reading the schedule: ")
                print "Check again in ... ", config['CHECK_EVERY_SEC'], "seconds"
                time.sleep(config['CHECK_EVERY_SEC'])
                continue
            #check if it's the lecture number we want to alert
            for lec in c_info["lectures"]:
                if int(lec["sec"]) == C_ALERTS['lec_num']:
                
                    #parse based on lecture enrollment
                    if C_ALERTS['sec_num'] == "all":
                        #section is open
                        if int(lec["enroll_total"]) < int(lec["enroll_cap"]):
                            msg = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n"\
                                  " Class: " +C_ALERTS['major']+' '+C_ALERTS["course"]+ \
                                  " Lecture: " + str(C_ALERTS['lec_num']) + "  Section: " + C_ALERTS['sec_num']+\
                                  " is open! \n Status: " + str(lec["enroll_total"]) + " / " + str(lec["enroll_cap"])
                            sendAlert(msg)
                            config['CLASSES_ALERT'].remove(C_ALERTS)
                        else:
                            print "not open"
                    
                    #parse based on section enrollment
                    else:
                        #check if it's the section number we want to alert
                        for sec in lec["class_sections"]:
                            if sec["sec"] == C_ALERTS['sec_num']:
                                #section is open
                                if int(sec["enroll_total"]) < int(sec["enroll_cap"]):
                          
                                    msg = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + \
                                      " Class: " +C_ALERTS['major']+' '+C_ALERTS["course"]+ \
                                      " Lecture: " + str(C_ALERTS['lec_num']) + "  Section: " + C_ALERTS['sec_num']+\
                                      " is open! \n Status: " + str(sec["enroll_total"]) + " / " + str(sec["enroll_cap"])
                                    sendAlert(msg)
                                    config['CLASSES_ALERT'].remove(C_ALERTS)
                                else:
                                    print "not open"


                    
        #check every 15 seconds
        time.sleep(config['CHECK_EVERY_SEC'])
