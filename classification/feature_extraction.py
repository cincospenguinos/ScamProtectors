from sklearn import linear_model
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
import random
import re
import os

"""
Takes in the raw
"""
def parse_corpora(examples):
    email_texts = []
    curr_email = str(examples[0])

    for i in range(1, len(examples)):
        line = str(examples[i])
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
    email = {'email_body_text': '', 'label': 1}

    for em in email_texts:
        for line in em.splitlines():
            if header_re.match(line):
                email[line.split()[0]] = ' '.join(line.split()[1:])
            else:
                email['email_body_text'] += line + '\n'
        emails.append(email)
        email = {'email_body_text': '', 'label': 1}

    return emails


# def email_body_next(examples, start):
#     header_re = re.compile(r"[a-zA-Z-]*: ")
#
#     is_body = True
#
#     for x in range(start+1, start+6):
#         if header_re.match(examples[x]):
#             is_body = False
#
#     return is_body


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


def strip_html(body_text):
    soup = BeautifulSoup(body_text, 'lxml')
    data = soup.findAll(text=True)

    #result = filter(visible, data)

    return '\n'.join(data)


def strip_non_words(emails):
    with open('/usr/share/dict/words') as f:
        eng_dic_raw = f.read()

    eng_set = set()

    for word in eng_dic_raw.split():
        eng_set.add(word.lower())

    for em in emails:
        scrubbed = ''
        for word in em['email_body_processed'].split():
            if word in eng_set:
                scrubbed += word + ' '
        em['email_body_processed'] = scrubbed


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

    num_samples = 0

    with open("dataset/nigerian_prince_emails.txt") as f:
        examples = f.read().splitlines()[1:]

    print("Parsing Scam EMails")
    email_texts = parse_corpora(examples)

    print("Parsing Headers and Bodies")
    scam_emails = parse_emails(email_texts)

    print("Number of EMails Processed: " + str(len(scam_emails)))

    print("Stripping HTML from EMails, Converting to Lower Case for Comparisons (This may take a few minutes)")
    for em in scam_emails:
        em['email_body_processed'] = strip_html(em['email_body_text']).lower()

    # encrypted_count = 0
    # for em in emails:
    #     if detect_encrypted(em['email_body_text']):
    #         encrypted_count += 1
    #
    # print("Encrypted EMails: " + str(encrypted_count))

    print("Stripping Non-Words from the EMail Bodies")
    strip_non_words(scam_emails)

    print("Sampling from the Processed Corpus")

    for x in range(num_samples):
        random_index = random.randint(0, len(scam_emails))
        random_email = scam_emails[random_index]
        print("Random EMail #" + str(random_index) + '\n')
        print("Original EMail Body: \n")
        print(random_email['email_body_text'] + '\n')
        print("Processed EMail Body: \n")
        processed_email = random_email['email_body_processed'].split()
        line = ''
        for x in range(len(processed_email)):
            line += processed_email[x] + ' '
            if x % 15 == 0:
                print(line)
                line = ''

    print("Processing Non-Scam EMails")
    non_scam_emails = []

    rel = 'dataset/spam_assasin_ham'
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, rel)
    for file in os.listdir(filename):
        with open(rel + '/' + file) as text:
            non_scam_emails.append({'email_body_text': text.read().decode("utf-8"), 'label': 0})

    print("Number of EMails Processed: " + str(len(non_scam_emails)))

    print("Stripping HTML from EMails, Converting to Lower Case for Comparisons (This may take a few minutes)")
    for em in non_scam_emails:
        em['email_body_processed'] = strip_html(em['email_body_text']).lower()

    print("Stripping Non-Words from the EMail Bodies")
    strip_non_words(non_scam_emails)

    print("Sampling from the Processed Corpus")

    for x in range(num_samples):
        random_index = random.randint(0, len(non_scam_emails))
        random_email = non_scam_emails[random_index]
        print("Random EMail #" + str(random_index) + '\n')
        print("Original EMail Body: \n")
        print(random_email['email_body_text'] + '\n')
        print("Processed EMail Body: \n")
        processed_email = random_email['email_body_processed'].split()
        line = ''
        for x in range(len(processed_email)):
            line += processed_email[x] + ' '
            if x % 15 == 0:
                print(line)
                line = ''

    all_emails = scam_emails + non_scam_emails
    random.shuffle(all_emails)

    split = int(len(all_emails) * 0.8)

    train_data = []
    test_data = []

    for i in range(split):
        train_data.append(all_emails[i])

    for i in range(split, len(all_emails)):
        test_data.append(all_emails[i])

    vector_data_text = []
    label_data = []

    for em in train_data:
        vector_data_text.append(em['email_body_processed'])
        label_data.append(em['label'])

    classifier = linear_model.SGDClassifier()

    vectorizer = CountVectorizer(analyzer=str.split)

    vector_data = vectorizer.fit_transform(vector_data_text)

    print(vectorizer.get_feature_names())

    classifier.fit(vector_data, label_data)

    num_correct = 0
    for test in test_data:
        vector_data = vectorizer.fit_transform([test['email_body_processed']])
        result = classifier.predict(vector_data)[0]
        if result == test['label']:
            num_correct += 1

    print("After Training and Testing " + str(num_correct/len(test_data)) + " of EMails were correctly classified.")


if __name__ == "__main__":
    main()
