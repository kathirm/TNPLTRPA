import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication



def sendmail(studEmail, userId, randomPwd):
    try:
        smtp_ssl_host = 'smtp.gmail.com'
        smtp_ssl_port = 465
        username = 'terafastnetworkteam@gmail.com'
        password = 'abcd@12345'
        sender = 'terafastnetworkteam@gmail.com'
        targets = ['technical@maher.ac.in',studEmail]

        msg = MIMEMultipart()
        msg['Subject'] = 'Login Credentials'
        msg['From'] = sender
        msg['To'] = ', '.join(targets)

        content = "Dear Student<br></br> Login ID: %s </br> Password : %s </br></br></br> <font color='red'>Note: Please ignore the previous email that you received with username and password and use this instead.</font></br> </br> Thanks & Regards </br> MAHER SUPPORT TEAM"%(userId, randomPwd)

        txt = MIMEText(content, 'html')
        msg.attach(txt)

        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(username, "abcd@12345")
        server.sendmail(sender, targets, msg.as_string())
        server.quit()
    except Exception as er:
        print "[WARNING] SEND MAIL FUNCTION EXCEPTION ERROR :: %s"%er


if __name__ == "__main__":

    sendmail()
