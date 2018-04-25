'''
monitor_vtus.py
Monitors the emails of all VTUs in our DB. Times how long it takes to manage each one.
Intended to be used with cron. I don't really know what else to say here.
'''
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from sklearn import linear_model
from sklearn.externals import joblib
import pymysql
import base64

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = [
	'https://www.googleapis.com/auth/gmail.modify'
]
CLIENT_SECRET_FILE = 'client_secret.json'
CLASSIFIER_FILE = 'bow_classifier.joblib.pkl'

def get_classifier():
	'''Gets the serialized classifier from the local directory.
	'''
	return joblib.load(CLASSIFIER_FILE)

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
	credential_path = os.path.join(credential_dir, 'scam-protectors-credentials.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = 'Scam Protectors'
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

def get_db_connection():
	return pymysql.connect(user=os.environ['SP_DATABASE_USERNAME'], password=os.environ['SP_DATABASE_PASSWORD'], host=os.environ['SP_DATABASE_HOST'], database=os.environ['SP_DATABASE_SCHEMA'])

def main():
	classifier = get_classifier()
	db_connection = get_db_connection()
	credentials = get_credentials()

	cursor = db_connection.cursor()
	cursor.execute('SELECT TOKEN FROM user_token WHERE vtu_email = "2018scamprotectors@gmail.com"')
	token = cursor.fetchone()[0]

	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)

	msgs = service.users().messages().list(userId='me').execute()

	while True:
		for msg in msgs['messages']:
			mail_id = msg['id']
			mail = service.users().messages().get(userId='me', id=mail_id, format='full').execute()
			
			for part in mail['payload']['parts']:
				body = base64.urlsafe_b64decode(part['body']['data'].encode('UTF-8'))
				print(body)

			# TODO: Check with the classifier
			if False:
				# TODO: query = ("INSERT INTO flagged_emails (USER_ID, SUBJECT, TOKEN_ID) VALUES (57, '{0}', 29);".format(subject))
				service.users().messages().trash(userId='me', id=mail_id).execute()
			else:
				print('All good.')

		if 'nextPageToken' in msgs:
			msgs = service.users().messages().list(userId='me', pageToken=msgs['nextPageToken']).execute()
		else:
			break


if __name__ == '__main__':
	main()