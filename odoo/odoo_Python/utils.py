import json, sys
import os, smtplib
from configparser import ConfigParser
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def read_config():
    try:
        cfgFile = '/home/kathir/odoo_Python/odoomail.cfg'
        config = ConfigParser()
        config.read(cfgFile)
        mailConfig = {}
        mailConfig['smtp_host'] = config['mailconfiguration']['smtp_host']
        mailConfig['smtp_port'] = config['mailconfiguration']['smtp_port']
        mailConfig['username']  = config['mailconfiguration']['username']
        mailConfig['password']  = config['mailconfiguration']['password']
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
        subject  = mail_info['subject'];

        sender  = mail_info['username'];
        msg = MIMEMultipart()
        msg['From'] = sender;
        msg['To'] = targets;

        if subject is not None:
            msg['Subject'] = subject;

        if body is not None:
            txt = MIMEText(body, 'html')
            msg.attach(txt)

        if attachment_file_path is not None:
            filepath = attachment_file_path;
            with open(filepath, 'rb') as f:
                docx = MIMEApplication(f.read())
            docx.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath))
            msg.attach(docx)

        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(username, password)
        server.sendmail(sender, targets, msg.as_string())
        server.quit()
        print("\n [SUCCESS] MAIL NOTIFICATION ALERT SEND SUCCESSFULLY :: %s"%targets)

    except Exception as er:
        print("\n [WARNING] SEND EMAIL NOTIFICATIONE ALERT EXCEPTION :: %s"%er)

