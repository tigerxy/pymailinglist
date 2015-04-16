#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import imaplib
import getpass
import email
import datetime
import smtplib

from mailerconfig import *
import mailerlib

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
    
    if message['Subject'] is None:
        message['Subject'] = ""
	
    if mail.endswith(smtpHost):
        imap.copy(mailnr, 'INBOX.fehler')
        imap.store(mailnr, '+FLAGS', '\\Deleted')
	imap.expunge()

        sentError += 1
    elif mail.lower() not in mailingList:
        # replace headers (could do other processing here)
        #message.add_header('Reply-To', fromAddress)
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
        #message.add_header('Reply-To', fromAddress)
        message.replace_header("Subject", "[" + listName + "] " + message['Subject'])

        imap.copy(mailnr, 'INBOX.gesendet')
        imap.store(mailnr, '+FLAGS', '\\Deleted')
	
	imap.expunge()
        # open authenticated SMTP connection and send message with
        # specified envelope from and to addresses
        for toAddress in mailingList:
            message.replace_header("To", toAddress)
            smtp.sendmail(fromAddress, toAddress, message.as_string())

        sentOk += 1

if sentOk != 0 and sentNotInList != 0 and sentError != 0:    
	print sentOk, "mail moved to INBOX.gesendet"
	print sentNotInList, "mail moved to INBOX.nichtinverteiler"
	print sentError, "mail moved to INBOX.fehler"

        for toAddress in mailingList:
                print toAddress, "\n"

imap.expunge()
imap.close()
mailerlib.imap_close(imap)
mailerlib.smtp_close(smtp)
