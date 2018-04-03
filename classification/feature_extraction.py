from sklearn import linear_model
from sklearn.feature_extraction import DictVectorizer
import random
import re


def parse_corpora(examples):
    email_texts = []
    curr_email = examples[0]

    for i in range(1, len(examples)):
        line = examples[i]
        if line.split():
            if line.split()[0] == 'Return-Path:':
                email_texts.append(curr_email)
                curr_email = line + '\n'
            else:
                curr_email += line + '\n'

    return email_texts


def parse_emails(email_texts):
    emails = []
    header_re = re.compile(r"[a-zA-Z-]*: ")
    email = {'email_body_text': ''}

    for em in email_texts:
        for line in em.splitlines():
            if header_re.match(line):
                email[line.split()[0]] = ' '.join(line.split()[1:])
            else:
                email['email_body_text'] += line + '\n'
        emails.append(email)
        email = {'email_body_text': ''}

    return emails


def email_body_next(examples, start):
    header_re = re.compile(r"[a-zA-Z-]*: ")

    is_body = True

    for x in range(start+1, start+6):
        if header_re.match(examples[x]):
            is_body = False

    return is_body


def detect_word(eng_set, word):
    if word in eng_set:
        return True
    else:
        return False


def detect_html(email_body):

    if email_body.count('<') > 5:
        return True
    else:
        return False


def detect_encrypted(email_body):
    encrypted = False
    words = email_body.split()
    for word in words:
        if len(word) > 30:
            encrypted = True
    return encrypted


def get_random_email():
    return 0


def main():

    classifier = linear_model.SGDClassifier()

    with open("dataExtraction/data/fradulent_emails.txt") as f:
        examples = f.read().splitlines()[1:]

    email_texts = parse_corpora(examples)

    emails = parse_emails(email_texts)

    print("Number of EMails: " + str(len(emails)))

    html_count = 0
    for em in emails:
        if detect_html(em['email_body_text']):
            html_count += 1
            #print(em['email_body_text'])

    print("HTML EMails: " + str(html_count))

    encrypted_count = 0
    for em in emails:
        if detect_encrypted(em['email_body_text']):
            encrypted_count += 1

    print("Encrypted EMails: " + str(encrypted_count))

    # random_email = emails[random.randint(0, len(emails))]
    # print("Random EMail: \n")
    #
    # for key in random_email.keys():
    #     print('Key: ' + key)
    #     print('Val: ' + str(random_email[key]))

    with open('/usr/share/dict/words') as f:
        eng_dic_raw = f.read()

    eng_set = set()

    for word in eng_dic_raw.split():
        eng_set.add(word)

    print(emails[127]['email_body_text'])

    scrubbed = ''

    for word in emails[127]['email_body_text'].split():
        if detect_word(eng_set, word):
            scrubbed += word + ' '

    print(scrubbed)

    vectorizer = DictVectorizer()

    vector_data = vectorizer.fit_transform(emails)

    print(vector_data.toarray())

    regr = linear_model.SGDClassifier()

    #regr.fit(vector_data)


if __name__ == "__main__":
    main()
