#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

#import cgi

import sys
import imaplib
import getpass
import email
import datetime
import smtplib

from mailerconfig import *

def header(title):
    print 'Content-type: text/html\n'
    print '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8"><title>%s</title>\n</head>\n<body>\n' % (title)

def footer():
    print "\n</body>\n</html>"
    
print "Content-Type: text/html"
header("Mails verarbeiten")

fehler = 0
nichtinverteiler = 0
gesendet = 0

smtp = smtplib.SMTP(host)
smtp.starttls()
smtp.login(user, passwd)

imap = imaplib.IMAP4_SSL(host)
imap.login(user, passwd)

imap.select('INBOX')
status, daten = imap.search(None, "ALL") 
for mailnr in daten[0].split(): 
    typ, daten = imap.fetch(mailnr, "(RFC822)")
    
    # create a Message instance from the email data
    message = email.message_from_string(daten[0][1])

    from email.utils import parseaddr
    name, mail = parseaddr(message['From'])
	
    if mail.endswith(host):
        imap.copy(mailnr, 'INBOX.fehler')
        imap.store(mailnr, '+FLAGS', '\\Deleted')
        fehler += 1
    elif mail not in verteiler:
        # replace headers (could do other processing here)
        #message.replace_header("Reply-To", from_addr)
        message.add_header('Reply-To', from_addr)
        message.replace_header("Subject", "[CVJM-Forchheim][SPAM?] " + message['Subject'])

        # open authenticated SMTP connection and send message with
        # specified envelope from and to addresses
        for empfaenger in admins:
            message.replace_header("To", empfaenger)
            smtp.sendmail(from_addr, empfaenger, message.as_string())
            
        imap.copy(mailnr, 'INBOX.nichtinverteiler')
        imap.store(mailnr, '+FLAGS', '\\Deleted')
        nichtinverteiler += 1
    else:
        # replace headers (could do other processing here)
        #message.replace_header("Reply-To", from_addr)
        message.add_header('Reply-To', from_addr)
        message.replace_header("Subject", "[CVJM-Forchheim] " + message['Subject'])

        # open authenticated SMTP connection and send message with
        # specified envelope from and to addresses
        for empfaenger in verteiler:
            message.replace_header("To", empfaenger)
            smtp.sendmail(from_addr, empfaenger, message.as_string())

        imap.copy(mailnr, 'INBOX.gesendet')
        imap.store(mailnr, '+FLAGS', '\\Deleted')
        gesendet += 1
    
print "<p>", gesendet, "mail moved to INBOX.gesendet</p>"
print "<p>", nichtinverteiler, "mail moved to INBOX.nichtinverteiler</p>"
print "<p>", fehler, "mail moved to INBOX.fehler</p>"

imap.expunge()
imap.close()
imap.logout()

smtp.quit()
footer()
