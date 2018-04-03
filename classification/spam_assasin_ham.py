'''
spam_assasin_ham.py

Gather up all of the spam assasin ham emails.
'''
import os
from email import *

'''
get_all_emails()

Returns all ham emails from spam assasin.
'''
def get_all_emails():
	collection = []
	names = os.listdir('dataset/spam_assasin_ham')
	for name in names:
		with open('dataset/spam_assasin_ham/' + name, 'r') as f:
			text = f.readlines()
			relevant_text = ''
			flag = False

			for line in text:
				if flag:
					relevant_text += line
				if 'Message-ID' in line:
					flag = True

			var1 = Email(relevant_text, 0)
			collection.append(var1)

	return collection

def main():
	emails = get_all_emails()

if __name__ == "__main__":
	main()