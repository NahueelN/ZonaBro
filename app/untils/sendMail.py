from email.message import EmailMessage
import ssl
import smtplib

email_sender = "argenbroinfo@gmail.com"
password = "bhmq mdcl pjzr dsgi"

def sendEmail(email_reciver,subject,body):
    
    em= EmailMessage()
    em["From"]=email_sender
    em["To"]=email_reciver
    em["Subject"]=subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com",465,context= context) as smtp:
        smtp.login(email_sender,password)
        smtp.sendmail(email_sender,email_reciver,em.as_string())