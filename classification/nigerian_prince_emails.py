# nigerian_prince_emails.py
'''
A set of functions to convert the nigerian prince email corpus into a nicer, more easily usable format
to interact with.
'''

def get_all_emails():
	emails = []

	with open("dataset/nigerian_prince_emails.txt") as f:
		herp = f.readlines()
		print(herp)

	return emails


def main():
	emails = get_all_emails()
	print(emails)

if __name__ == "__main__":
	main()
