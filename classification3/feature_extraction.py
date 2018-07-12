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
    # with open('/usr/share/dict/words') as f:
    #     eng_dic_raw = f.read()

    with open('words.txt') as f:
        eng_dic_raw = f.read()

    eng_set = set()

    for word in eng_dic_raw.split():
        if not_classifier_flag(word.lower()):
            eng_set.add(word.lower())

    for em in emails:
        scrubbed = ''
        for word in em['email_body_processed'].split():
            if word in eng_set:
                scrubbed += word + ' '
        em['email_body_processed'] = scrubbed


def not_classifier_flag(string):
    classifier_flags = {'id', 'imap'}
    if string in classifier_flags:
        return False
    if len(string) < 2:
        return False
    return True


def print_sample(sample, index=-1):
    sample_string = ''
    if index == -1:
        sample_string += "Incorrectly Labeled EMail" + '\n'
    else:
        sample_string += "Random EMail #" + str(index) + '\n'
    sample_string += "Label: " + str(sample['label']) + '\n'
    if 'prediction' in list(sample):
        sample_string += "Prediction: " + str(sample['prediction']) + '\n'
    sample_string += "Processed EMail Body: \n"
    processed_email = sample['email_body_processed'].split()
    line = ''
    for x in range(len(processed_email)):
        line += processed_email[x] + ' '
        if x % 15 == 0:
            sample_string += line + '\n'
            line = ''
    sample_string += "\nOriginal EMail Body: \n"
    sample_string += sample['email_body_text'] + '\n'
    return sample_string


def log_samples(data, num_samples, num_scam):
    sample_log = ''
    sample_log += "#####################################\n" \
                  "# LOG: SAMPLES FROM PROCESSED EMAILS\n" \
                  "#####################################\n"
    sample_log += "##############\n" \
                  "# SCAM EMAILS\n" \
                  "##############\n"
    for x in range(num_samples):
        random_index = random.randint(0, num_scam)
        random_email = data[random_index]
        sample_log += print_sample(random_email, index=random_index)
    sample_log += "##################\n" \
                  "# NON-SCAM EMAILS\n" \
                  "##################\n"
    for x in range(num_samples):
        random_index = random.randint(num_scam, len(data))
        random_email = data[random_index]
        sample_log += print_sample(random_email, index=random_index)
    with open('samples.log', 'w') as f:
        f.write(sample_log)


def log_features(features, weights):
    pairs = {}

    for feature in range(len(features)):
        pairs[features[feature]] = weights[feature]

    feature_log = ''
    feature_log += "#######################################\n" \
                  "# LOG: BEST FEATURES IN THE CLASSIFIER\n" \
                  "#######################################\n"
    feature_log += "\nTop 10 Features for identifying a scam email: \n"
    for x in range(10):
        max_feature = max(pairs, key=pairs.get)
        feature_log += max_feature + '\n'
        feature_log += str(pairs[max_feature]) + '\n'
        pairs.pop(max_feature)

    feature_log += "\nTop 10 Features for identifying a non-scam email: \n"
    for x in range(10):
        min_feature = min(pairs, key=pairs.get)
        feature_log += min_feature + '\n'
        feature_log += str(pairs[min_feature]) + '\n'
        pairs.pop(min_feature)

    with open('features.log', 'w') as f:
        f.write(feature_log)


def main():

    #######################
    # Process Scam E-Mails
    #######################

    with open("dataset/nigerian_prince_emails.txt") as f:
        examples = f.read().splitlines()[1:]

    print("\nParsing Scam EMails")
    email_texts = parse_corpora(examples)

    print("Parsing Headers and Bodies")
    scam_emails = parse_emails(email_texts)

    num_scam = len(scam_emails)

    ###########################
    # Process Non-Scam E-Mails
    ###########################

    print("\nProcessing Non-Scam EMails")
    non_scam_emails = []

    print("Processing Ham EMails")

    rel = 'dataset/spam_assasin_ham'
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, rel)
    for file in os.listdir(filename):
        with open(rel + '/' + file) as text:
            non_scam_emails.append({'email_body_text': text.read(), 'label': 0})

    print("Processing Enron EMails")

    rel = 'dataset/EnronRandom-Minorthird'
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, rel)
    for file in os.listdir(filename):
        with open(rel + '/' + file) as text:
            non_scam_emails.append({'email_body_text': text.read(), 'label': 0})

    print("Processing NewsGroups EMails")

    rel = 'dataset/NewsGroups-Minorthird'
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, rel)
    for file in os.listdir(filename):
        with open(rel + '/' + file) as text:
            non_scam_emails.append({'email_body_text': text.read(), 'label': 0})

    num_non_scam = len(non_scam_emails)

    ####################
    # COMBINE DATA SETS
    ####################

    all_emails = scam_emails + non_scam_emails

    print("\nStripping HTML from EMails, Converting to Lower Case for Comparisons (This may take a few minutes)")
    for em in all_emails:
        em['email_body_processed'] = strip_html(em['email_body_text']).lower()

    print("Stripping Non-Words from the EMail Bodies")
    strip_non_words(all_emails)

    print("\nLogging Scam and Non-Scam Samples from the Processed Corpus")

    log_samples(all_emails, 3, num_scam)

    ##################################
    # CREATE TRAIN AND TEST DATA SETS
    ##################################

    random.shuffle(all_emails)

    split = int(len(all_emails) * 0.8)

    train_data = []
    test_data = []

    for i in range(split):
        train_data.append(all_emails[i])

    for i in range(split, len(all_emails)):
        test_data.append(all_emails[i])

    ###################
    # TRAIN CLASSIFIER
    ###################

    print("\nTraining the classifier")
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
    print("Storing classifier as " + filename)

    _ = joblib.dump(classifier, filename, compress=3)

    ##################
    # LOAD CLASSIFIER
    ##################

    classifier = joblib.load(filename)

    #######################
    # ANALYZE TOP FEATURES
    #######################

    print("\nLogging feature analysis")
    features = vectorizer.get_feature_names()
    weights = classifier.coef_[0]
    log_features(features, weights)

    ####################################
    # TEST CLASSIFIER AGAINST TEST DATA
    ####################################

    print("\nTesting Classifier and Logging Failed Predictions")
    num_correct = 0
    num_predicted_scam = 0
    num_labeled_scam = 0
    fails_log = ''
    fails_log += "#########################################\n" \
                  "# LOG: ALL INCORRECTLY PREDICTED EMAILS\n" \
                  "########################################\n"
    for test in test_data:
        vector_data = vectorizer.transform([test['email_body_processed']])
        result = classifier.predict(vector_data)[0]
        test['prediction'] = result
        if test['label'] == 1:
            num_labeled_scam += 1
        if test['prediction'] == 1:
            num_predicted_scam +=1
        if result == test['label'] == 1:
            num_correct += 1
        elif result != test['label']:
            fails_log += print_sample(test) + '\n'

    with open('fails.log', 'w') as f:
        f.write(fails_log)

    precision = num_correct / num_predicted_scam
    recall = num_correct / num_labeled_scam

    print("\nWith a corpus of " + str(num_scam) + " Scam emails and " + str(num_non_scam) + " Non-Scam emails")
    print("After Training with " + str(len(train_data)) + " emails and Testing with " + str(len(test_data)) + " emails")
    print("Emails were correctly classified with: \n")
    print("Precision: " + str(precision))
    print("Recall: " + str(recall))
    print("F-Score: " + str(2*precision*recall/(precision+recall)))


if __name__ == "__main__":
    main()
