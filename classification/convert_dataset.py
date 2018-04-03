'''
convert_dataset.py

Convert the dataset from the version that we have into a DB that we can query
and do fancy shiz with.
'''
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

import sp_email
from spam_assasin_ham import spam_assasin_ham_get_all_emails

def main():
	local_db_username = os.environ['SP_SCHEMA_NAME']
	local_db_password = os.environ['SP_SCHEMA_PASSWORD']

	if local_db_username is None or local_db_password is None:
		print('$SP_SCHEMA_NAME or $SP_SCHEMA_PASSWORD is not set! Set these variables before attempting to convert the dataset!')

	engine = create_engine('mysql://' + local_db_username + ':' + local_db_password + '@localhost:3306/scam_protectors')
	declarative_base().metadata.create_all(engine)

	ham = spam_assasin_ham_get_all_emails()

	## TODO: Put this into a local database


if __name__ == '__main__':
	main()