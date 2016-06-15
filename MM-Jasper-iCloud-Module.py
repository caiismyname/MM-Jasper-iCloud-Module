# Gmail imports
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

# iCloud imports
import re
from pyicloud import PyiCloudService

from time import sleep

# For iCloud API
api = PyiCloudService('davidcai2012@gmail.com','cilantroLime7.03')
iphone = api.devices['cetbS6ENhf8TSwHWRSpwmcI8L3J+C3USnmt6gCjV05FdE2jKVT8dNeHYVNSUzmWV']

# For Jasper
WORDS = ["IPHONE", "FIND"]

# For Gmail
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


# Jasper functions
def isValid(text):
	# Seperate, all valid triggers
	one = bool(re.search(r'\bIPHONE\b', text, re.IGNORECASE))
	two = bool(re.search(r'\bFIND\b', text, re.IGNORECASE))

	if one or two:
		return True
	else:
		return False

def handle(text, mic, profile):
	iphone.play_sound()
	mic.say("Sounding")

	sleep(10)
	googleInit()


def googleInit():
	"""
	Shell function. This calls the google login functions, which then call the 
	mailParseDelete function to delete the emails sent b/c Find My iPhone has
	been called. 
	"""

	try:
	    import argparse
	    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
	except ImportError:
	    flags = None

	mailParseTrash()


def get_credentials():
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
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def mailParseTrash():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # Gets messages from apple that are unread
    results = service.users().messages().list(userId='me', q="from:noreply@insideicloud.icloud.com, is:unread").execute()
    if 'messages' in results:
    	emails = results['messages']
    	for x in emails:
	    	xId = x['id']
	    	# Marks messages as read and in trash
	    	service.users().messages().modify(userId='me', id=xId, body={'addLabelIds':['TRASH'], 'removeLabelIds':['UNREAD', "INBOX"]}).execute()

