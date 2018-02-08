


with open("fradulent_emails.txt") as f:
    examples = f.read()

emails = []
email = ''

for line in examples.splitlines():
    if line[:7] == "From r " and len(email) > 0:
        print("Start new e-mail")
        emails.append(email)
        email = line + '\n'
    else:
        email += line + '\n'

