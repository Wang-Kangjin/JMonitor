import os, sys, string
import smtplib
#!/usr/bin/python
# -*- coding: utf-8 -*-


import smtplib
from email.mime.text import MIMEText

#####################
#
mail_host="smtp.gmail.com"
mail_user="kangjin.wang"
mail_pass="WKJ@18734869733"
mail_postfix="gmail.com"

######################
def send_mail(to_list,sub,content):
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP(mail_host)
        s.set_debuglevel(1)
        s.ehlo()
        s.starttls()
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

