from __future__ import print_function
import httplib2
import os
import argparse
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

class GMail(object):
    SCOPES = 'https://www.googleapis.com/auth/gmail.send'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'canvas gadget'
    DEFAULT_SENDER = 'support@canvasgadget.com'
    
    def __init__(self, sender=None):
        self.sender = sender if sender else self.DEFAULT_SENDER
        
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)
    
    def _get_credentials(self):
        """Gets valid user credentials from storage.
    
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
    
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'gmail-canvas-gadget.json')
    
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run_flow(flow, store, argparse.Namespace(
                auth_host_name = 'localhost', 
                auth_host_port = [8080, 8090], 
                logging_level = 'ERROR', 
                noauth_local_webserver = False
                )
            )
        return credentials
    
    def _create_message(self, to, subject, message_text):
        """Create a message for an email.
        
        Args:
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.
        
        Returns:
          An object containing a base64url encoded email object.
        """
        message = MIMEMultipart('')
        message['to'] = to
        message['from'] = self.sender
        message['subject'] = subject
        message.attach(MIMEText(message_text, 'html'))
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}
    
    def _send_message(self, message, user_id='me'):
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
            message = (self.service.users().messages().send(userId=user_id, body=message).execute())
            return message
        except Exception as error:
            print ('An error occurred: {0}'.format(error))
            
    def send_email(self, to, subject, message_text):
        message = self._create_message(to, subject, message_text)
        self._send_message(message)