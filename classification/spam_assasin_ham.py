'''
spam_assasin_ham.py

Gather up all of the spam assasin ham emails.
'''
import os
from email import *

def get_all_emails():
	collection = []
	names = os.listdir('dataset/spam_assasin_ham')
	for name in names:
		with open('dataset/spam_assasin_ham/' + name, 'r', encoding='ascii') as f:
			text = f.read()
			mail = Email(text, 0)
			collection.append(mail)

	return collection

def main():
	get_all_emails()

if __name__ == "__main__":
	main()