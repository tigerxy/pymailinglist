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
import mailerlib

def header(title):
    print 'Content-type: text/html\n'
    print '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8"><title>%s</title>\n</head>\n<body>\n' % (title)

def footer():
    print "\n</body>\n</html>"
    
print "Content-Type: text/html"
header("Mails verarbeiten")

sentOk = 0
sentNotInList = 0
sentError = 0

smtp = mailerlib.smtp_open()
imap = mailerlib.imap_open()

imap.select('INBOX')
status, daten = imap.search(None, "ALL") 
for mailnr in daten[0].split(): 
    typ, daten = imap.fetch(mailnr, "(RFC822)")
    
    # create a Message instance from the email data
    message = email.message_from_string(daten[0][1])

    from email.utils import parseaddr
    name, mail = parseaddr(message['From'])
	
    if mail.endswith(smtpHost):
        imap.copy(mailnr, 'INBOX.fehler')
        imap.store(mailnr, '+FLAGS', '\\Deleted')
        sentError += 1
    elif mail not in mailingList:
        # replace headers (could do other processing here)
        #message.replace_header("Reply-To", from_addr)
        message.add_header('Reply-To', fromAddress)
        message.replace_header("Subject", "[" + listName + "][SPAM?] " + message['Subject'])

        # open authenticated SMTP connection and send message with
        # specified envelope from and to addresses
        for toAddress in adminsList:
            message.replace_header("To", toAddress)
            smtp.sendmail(fromAddress, toAddress, message.as_string())
            
        imap.copy(mailnr, 'INBOX.nichtinverteiler')
        imap.store(mailnr, '+FLAGS', '\\Deleted')
        sentNotInList += 1
    else:
        # replace headers (could do other processing here)
        #message.replace_header("Reply-To", from_addr)
        message.add_header('Reply-To', fromAddress)
        message.replace_header("Subject", "[" + listName + "] " + message['Subject'])

        # open authenticated SMTP connection and send message with
        # specified envelope from and to addresses
        for toAddress in mailingList:
            message.replace_header("To", toAddress)
            smtp.sendmail(fromAddress, toAddress, message.as_string())

        imap.copy(mailnr, 'INBOX.gesendet')
        imap.store(mailnr, '+FLAGS', '\\Deleted')
        sentOk += 1
    
print "<p>", sentOk, "mail moved to INBOX.gesendet</p>"
print "<p>", sentNotInList, "mail moved to INBOX.nichtinverteiler</p>"
print "<p>", sentError, "mail moved to INBOX.fehler</p>"

imap.expunge()
imap.close()
mailerlib.imap_close(imap)
mailerlib.smtp_close(smtp)

footer()
