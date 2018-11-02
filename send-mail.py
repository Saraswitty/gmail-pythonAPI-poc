from __future__ import print_function
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
import base64
from google.oauth2 import service_account
from oauth2client import file, client, tools
import email.encoders
import mimetypes
from email.mime.base import MIMEBase
import os

'''
TODO Check how to sign emails so that the gmail web client does not show phishing warning
'''

EMAIL_FROM = 'ajaynair59@gmail.com'
EMAIL_TO = 'ajaynair59@gmail.com'
EMAIL_SUBJECT = 'Automated email'
EMAIL_CONTENT = 'Some content'

def create_message_with_attachment(
    sender, to, subject, message_text, file):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  main_type, sub_type = content_type.split('/', 1)
  fp = open(file, 'rb')
  msg = MIMEBase(main_type, sub_type)
  msg.set_payload(fp.read())
  fp.close()

  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  email.encoders.encode_base64(msg)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
  """Send an email message.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def service_account_login():
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service

service = service_account_login()

# Call the Gmail API
# Place file.pdf in the current dir. This is attached with the email.
message = create_message_with_attachment(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT, "file.pdf")
sent = send_message(service,'me', message)
