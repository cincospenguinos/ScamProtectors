'''
monitor_vtus.py

Monitors the emails of all VTUs in our DB. Times how long it takes to manage each one.
Intended to be used with cron. I don't really know what else to say here.
'''
from __future__ import print_function
import httplib2
import os
import sklearn

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

def get_classifier():
	'''Gets the serialized classifier from the local directory.
	'''
	print('This still needs to be done')
	return None

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

	store = Storage(credential_path)
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

def main():
	"""Shows basic usage of the Gmail API.

	Creates a Gmail API service object and outputs a list of label names
	of the user's Gmail account.
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)

	msgs = service.users().messages().list(userId='me').execute()
	
	if not msgs:
		print('Could not get any messages!')
	else:
		print('Cycling through messages...')
		
		classifier = get_classifier()

		while True:
			for msg in msgs['messages']:
				mail_id = msg['id']
				mail = service.users().messages().get(userId='me', id=mail_id).execute()

				# TODO: Check with the classifier
				if False:
					service.users().messages().trash(userId='me', id=mail_id).execute()

			if 'nextPageToken' in msgs:
				msgs = service.users().messages().list(userId='me', pageToken=msgs['nextPageToken']).execute()
			else:
				break


if __name__ == '__main__':
	main()