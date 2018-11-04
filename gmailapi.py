import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def gmail_api_init(username, password):
  global s
  s = smtplib.SMTP('smtp.gmail.com', 587)
  s.ehlo()
  s.starttls() 
  s.login(username, password) 

def send_email(email_from, email_to, cc, email_subject, email_content, attachment_file): 
  msg = MIMEMultipart() 
  msg['From'] = email_from
  msg['To'] = email_to
  msg['Cc'] = cc
  msg['Subject'] = email_subject
  msg.attach(MIMEText(email_content, 'plain'))  

  attachment = open(attachment_file, "rb")

  p = MIMEBase('application', 'octet-stream') 
  p.set_payload((attachment).read()) 
  encoders.encode_base64(p) 
  p.add_header('Content-Disposition', "attachment; filename= %s" % attachment_file) 
  msg.attach(p)

  msg_str = msg.as_string()
  s.sendmail("ajaynair59@gmail.com", "ajaynair59@gmail.com", msg_str) 
  
# terminating the session 
def gmail_api_fini():
   s.quit() 
