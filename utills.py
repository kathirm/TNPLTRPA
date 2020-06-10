import json, time, sys, os
import os, smtplib
from configparser import ConfigParser
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def read_config():
    try:
        cfgFile = '/etc/odoomail.cfg'
        config = ConfigParser()
        config.read(cfgFile)

        mailConfig = {}
        mailConfig['smtp_host'] = config['mailconfiguration']['smtp_host']
        mailConfig['smtp_port'] = config['mailconfiguration']['smtp_port']
        mailConfig['username']  = config['mailconfiguration']['username']
        mailConfig['password']  = config['mailconfiguration']['password']
	mailConfig['from_mail'] = config['mailconfiguration']['from_mail']
        mailConfig['subject']   = config['mailconfiguration']['subject']
    except Exception as er:
        print("\n [WARNING] READ MAIL NOTIFICATION CONFIGURATION FUNCTION EXCEPTION :: %s"%er)

    return mailConfig

def email_notification(targets, body=None,attachment_file_path=None):
    try:
        mail_info = read_config()
        smtp_ssl_host = mail_info['smtp_host'];
        smtp_ssl_port = int(mail_info['smtp_port']);
        username = mail_info['username'];
        password = mail_info['password'];
	fromMail = mail_info['from_mail'];
        subject  = mail_info['subject'];
        sender  = mail_info['username'];
        msg = MIMEMultipart('alternative') 
        msg['From'] = fromMail;
	msg['Subject'] = subject;
        msg['To'] = targets;

	mime_text = MIMEText(body, 'html')
	msg.attach(mime_text)

	server = smtplib.SMTP(smtp_ssl_host, smtp_ssl_port)
	server.starttls()
	server.login(username, password)
	server.sendmail(fromMail, targets, msg.as_string())
	server.quit()

	
        print("\n [SUCCESS] MAIL NOTIFICATION ALERT SEND SUCCESSFULLY :: %s"%targets.upper()+'\n')

    except Exception as er:
        print("\n [WARNING] SEND EMAIL NOTIFICATIONE ALERT EXCEPTION :: %s"%er)
