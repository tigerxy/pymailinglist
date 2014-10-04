#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgi
from mailerconfig import *

def header(title):
    print 'Content-type: text/html\n'
    print '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8"><title>%s</title>\n</head>\n<body>\n' % (title)

def footer():
    print "\n</body>\n</html>"

form = cgi.FieldStorage()
password = "python"

if not form:
    header("Login Response")
    print '''<FORM method="POST" action="?">
<paragraph> Enter your login name: <input type="text" name="login">
<paragraph> Enter your password: <input type=password name="password">
<paragraph> <input type="submit" value="Connect">
</FORM>
</CENTER>
<HR>

</form>'''
elif form.has_key("login") and form["login"].value != "" and form.has_key("password") and form["password"].value == password:
    header("Connected ...")
    print "<center><hr><H3>Welcome back," , form["login"].value, ".</H3><hr></center>"
    print r"""<form><input type="hidden" name="session" value="%s"></form>""" % (form["login"].value)
    print "<H3><a href=browse.html>Click here to start browsing</a></H3>"
    print verteiler
else:
    header("No success!")
    print "<H3>Please go back and enter a valid login.</H3>"

footer()
