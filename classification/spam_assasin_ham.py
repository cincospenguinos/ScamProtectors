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

	header_pattern = re.compile(r'^[\w-]+:\s*|From\s*\w+\@')
	url_pattern = re.compile(r'^(https?):\/\/[\w\-\_]+')

	for name in names:
		with open('dataset/spam_assasin_ham/' + name, 'r') as f:
			text = f.readlines()
			
			# Disregard all header info at the top of the email
			line_count = 0
			last_header = 0
			for idx in xrange(len(text)):
				line = text[idx]

				if re.match(header_pattern, line) and not re.match(url_pattern, line):
					last_header = idx
					line_count = 0
				else:
					line_count += 1

				if line_count == 4:
					break

			# Disregard all header info at the bottom of the email as well
			other_last_header = len(text)
			line_count = 0
			for idx in xrange(len(text) - 1, 0, -1):
				line = text[idx]

				if idx <= last_header or line_count == 2:
					break

				if re.match(header_pattern, line) and not re.match(url_pattern, line):
					other_last_header = idx
					line_count = 0
				else:
					line_count += 1

			# print(name + "\t" + str(last_header == other_last_header))

			relevant_text = ''

			for idx in range(len(text))[last_header + 1:other_last_header]:
				relevant_text += text[idx]

			# print(name + '\t' + str(not relevant_text))

			ham = ScamProtectorEmail(relevant_text, 0)
			collection.append(ham)

	return collection

def main():
	emails = spam_assasin_ham_get_all_emails()
	print(emails[3].full_text)

if __name__ == "__main__":
	main()