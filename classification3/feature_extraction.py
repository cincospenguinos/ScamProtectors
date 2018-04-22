from sklearn import linear_model
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
import random
import re
import os


def parse_corpora(examples):
    """
    Takes in the raw scam corpora and separates it into individual emails
    """
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
    """
    Takes in the separated email texts and parse the headers and the email body
    """
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


def strip_html(body_text):
    """
    Use beautiful soup to remove HTML tags from text
    """
    soup = BeautifulSoup(body_text, 'lxml')
    data = soup.findAll(text=True)

    return '\n'.join(data)


def strip_non_words(emails):
    """
    Check against english dictionary and remove non-words
    """
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


def main():

    num_samples = 0

    #######################
    # Process Scam E-Mails
    #######################

    with open("dataset/nigerian_prince_emails.txt", encoding="ISO-8859-1") as f:
        examples = f.read().splitlines()[1:]

    print("Parsing Scam EMails")
    email_texts = parse_corpora(examples)

    print("Parsing Headers and Bodies")
    scam_emails = parse_emails(email_texts)

    print("Number of EMails Processed: " + str(len(scam_emails)))

    print("Stripping HTML from EMails, Converting to Lower Case for Comparisons (This may take a few minutes)")
    for em in scam_emails:
        em['email_body_processed'] = strip_html(em['email_body_text']).lower()

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

    ###########################
    # Process Non-Scam E-Mails
    ###########################

    print("Processing Non-Scam EMails")
    non_scam_emails = []

    rel = 'dataset/spam_assasin_ham'
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, rel)
    for file in os.listdir(filename):
        with open(rel + '/' + file, encoding="ISO-8859-1") as text:
            non_scam_emails.append({'email_body_text': text.read(), 'label': 0})

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

    classifier = linear_model.SGDClassifier(max_iter=1000, tol=0.0001)

    vectorizer = CountVectorizer(analyzer=str.split)

    vector_data = vectorizer.fit_transform(vector_data_text)

    classifier.fit(vector_data, label_data)

    ###################
    # STORE CLASSIFIER
    ###################

    filename = 'bow_classifier.joblib.pkl'

    _ = joblib.dump(classifier, filename, compress=3)

    ##################
    # LOAD CLASSIFIER
    ##################
    
    classifier = joblib.load(filename)

    features = vectorizer.get_feature_names()
    weights = classifier.coef_[0]
    pairs = {}

    print(features)
    print(len(features))

    print(weights)
    print(len(weights))

    for feature in range(len(features)):
            pairs[features[feature]] = weights[feature]

    for x in range(20):
        max_feature = max(pairs, key=pairs.get)
        print(max_feature)
        print(pairs[max_feature])
        pairs.pop(max_feature)

    for x in range(20):
        min_feature = min(pairs, key=pairs.get)
        print(min_feature)
        print(pairs[min_feature])
        pairs.pop(min_feature)

    return

    num_correct = 0
    for test in test_data:
        vector_data = vectorizer.transform([test['email_body_processed']])
        result = classifier.predict(vector_data)[0]
        test['prediction'] = result
        if result == test['label']:
            num_correct += 1
        else:
            print("EMail Not Labeled Correctly:")
            print("Label: " + str(test['label']))
            print("Prediction: " + str(test['prediction']))
            print("Processed EMail Body:\n")
            processed_email = test['email_body_processed'].split()
            line = ''
            for x in range(len(processed_email)):
                line += processed_email[x] + ' '
                if x % 15 == 0:
                    print(line)
                    line = ''
            print()
            print("Original EMail Body:\n")
            print(test['email_body_text'])

    print("After Training with " + str(len(train_data)) + " emails")
    print("and Testing " + str(len(test_data)) + " emails")
    print(str(num_correct/len(test_data)) + " of emails were correctly classified.")

    for x in range(num_samples):
        random_index = random.randint(0, len(test_data))
        random_email = test_data[random_index]
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
        print("Label: " + str(random_email['label']))
        print("Prediction: " + str(random_email['prediction']))


if __name__ == "__main__":
    main()