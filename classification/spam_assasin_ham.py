'''
spam_assasin_ham.py

Gather up all of the spam assasin ham emails.
'''
import os
from sp_email import ScamProtectorEmail

'''
spam_assasin_ham_get_all_emails()

Returns all ham emails from spam assasin.
'''
def spam_assasin_ham_get_all_emails():
	collection = []
	names = os.listdir('dataset/spam_assasin_ham')
	for name in names:
		with open('dataset/spam_assasin_ham/' + name, 'r') as f:
			# TODO: Get all of the other pieces and include them in the constructor
			text = f.readlines()
			relevant_text = ''
			flag = False

			for line in text:
				if flag:
					relevant_text += line
				if 'Message-ID' in line:
					flag = True

			ham = ScamProtectorEmail(relevant_text, 0)
			collection.append(ham)

	return collection

def main():
	emails = spam_assasin_ham_get_all_emails()

if __name__ == "__main__":
	main()