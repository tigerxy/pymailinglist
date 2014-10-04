#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
#import cgitb
#cgitb.enable()

import sys
import imaplib
import getpass
import email
import datetime
import smtplib

from mailerconfig import *

def imap_open():
	con = imaplib.IMAP4_SSL(imapHost)
	con.login(imapUser, imapPassword)
	return con
    
def imap_close(con):
	con.logout()

def smtp_open():
	con = smtplib.SMTP(smtpHost)
	con.starttls()
	con.login(smtpUser, smtpPassword)
	return con

def smtp_close(con):
	con.quit()
