'''
spam_assasin_ham.py

Gather up all of the spam assasin ham emails.
'''
import os
import re
from sp_email import ScamProtectorEmail

'''
spam_assasin_ham_get_all_emails()

Returns all ham emails from spam assasin.
'''
def spam_assasin_ham_get_all_emails():
	collection = []
	names = os.listdir('dataset/spam_assasin_ham')

	header_pattern = re.compile(r'^[a-zA-Z]+:')

	for name in names:
		with open('dataset/spam_assasin_ham/' + name, 'r') as f:
			text = f.readlines()
			relevant_text = ''
			received_flag = False
			finished_flag = False

			for line in text:
				if re.match(header_pattern, line) and not finished_flag:
					if 'Received' in line:
						received_flag = True
					else:
						received_flag = False
				elif not received_flag:
					finished_flag = True

			ham = ScamProtectorEmail(relevant_text, 0)
			collection.append(ham)

	return collection

def main():
	emails = spam_assasin_ham_get_all_emails()
	print(emails[0].full_text)

if __name__ == "__main__":
	main()