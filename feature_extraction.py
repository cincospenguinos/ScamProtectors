from sklearn import linear_model
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import pickle
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


def parse_mbox(examples):
    """
        Takes in the raw email corpora and separates it into individual emails
        """
    email_texts = []
    curr_email = str(examples[0])

    header_re = re.compile(r"From [0-9][0-9][0-9]")

    for i in range(1, len(examples)):
        line = str(examples[i])
        if header_re.match(line):
            email_texts.append(curr_email)
            curr_email = line + '\n'
        else:
            curr_email += line + '\n'
        # if line.split():
        #     if line.split()[0] == 'From':
        #         email_texts.append(curr_email)
        #         curr_email = line + '\n'
        #     else:
        #         curr_email += line + '\n'

    return email_texts


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
    classifier_flags = {'id', 'imap', 'gmt'}
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
    sample_log += "LOG: SAMPLES FROM PROCESSED EMAILS\n"
    sample_log += "\nSCAM EMAILS\n"
    for x in range(num_samples):
        random_index = random.randint(0, num_scam)
        random_email = data[random_index]
        sample_log += print_sample(random_email, index=random_index)
    sample_log += "\nNON-SCAM EMAILS\n"
    for x in range(num_samples):
        random_index = random.randint(num_scam, len(data))
        random_email = data[random_index]
        sample_log += print_sample(random_email, index=random_index)
    with open('samples.log', 'wb') as f:
        f.write(sample_log.encode())


def log_features(features, weights):
    pairs = {}

    for feature in range(len(features)):
        pairs[features[feature]] = weights[feature]

    feature_log = ''
    feature_log += "LOG: BEST FEATURES IN THE CLASSIFIER\n"

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

    with open('features.log', 'wb') as f:
        f.write(feature_log.encode())


def main():

    with open('current.classifier.pkl', 'rb') as f:
        classif = pickle.load(f)

    print(classif)

    return

    #######################
    # Process Scam E-Mails
    #######################

    with open("dataset/nigerian_prince_emails.txt", encoding='latin-1') as f:
        examples = f.read().splitlines()[1:]

    print("\nParsing Scam EMails")
    email_texts = parse_corpora(examples)

    print("Parsing Headers and Bodies")
    scam_emails = parse_emails(email_texts)

    print("\nStripping HTML from EMails, Converting to Lower Case for Comparisons (This may take a few minutes)")
    for em in scam_emails:
        em['email_body_processed'] = strip_html(em['email_body_text']).lower()

    print("Stripping Non-Words from the EMail Bodies")
    strip_non_words(scam_emails)

    print("Removing Empty Emails")
    scam_emails = [em for em in scam_emails if len(em['email_body_processed'].split()) > 1]

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
        with open(rel + '/' + file, encoding='latin-1') as text:
            non_scam_emails.append({'email_body_text': text.read(), 'label': 0})

    print("Processing Enron EMails")

    rel = 'dataset/EnronRandom-Minorthird'
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, rel)
    for file in os.listdir(filename):
        with open(rel + '/' + file, encoding='latin-1') as text:
            non_scam_emails.append({'email_body_text': text.read(), 'label': 0})

    print("Processing NewsGroups EMails")

    rel = 'dataset/NewsGroups-Minorthird'
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, rel)
    for file in os.listdir(filename):
        with open(rel + '/' + file, encoding='latin-1') as text:
            non_scam_emails.append({'email_body_text': text.read(), 'label': 0})

    print("\nStripping HTML from EMails, Converting to Lower Case for Comparisons (This may take a few minutes)")
    for em in non_scam_emails:
        em['email_body_processed'] = strip_html(em['email_body_text']).lower()

    print("Stripping Non-Words from the EMail Bodies")
    strip_non_words(non_scam_emails)

    print("Removing Empty Emails")
    non_scam_emails = [em for em in non_scam_emails if em['email_body_processed'] != '']

    num_non_scam = len(non_scam_emails)

    ####################################
    # COMBINE DATA SETS AND LOG SAMPLES
    ####################################

    all_emails = scam_emails + non_scam_emails

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

    # Use class_weight to lower scam weighting
    classifier = linear_model.SGDClassifier(max_iter=1000, tol=0.0001)

    #vectorizer = CountVectorizer()
    vectorizer = TfidfVectorizer(ngram_range=(1, 3))

    vector_data = vectorizer.fit_transform(vector_data_text)

    # with open('current.vectorizer.pkl', 'wb') as f:
    #     pickle.dump(vectorizer, f)
    #
    # with open('current.vectorizer.pkl', 'rb') as f:
    #     vectorizer = pickle.load(f)

    filename = 'current.vectorizer.pkl'
    print("Storing vectorizer as " + filename)
    #_ = joblib.dump(vectorizer, filename)
    with open(filename, 'wb') as f:
        _ = pickle.dump(vectorizer, f)

    classifier.fit(vector_data, label_data)

    ###################
    # STORE CLASSIFIER
    ###################

    filename = 'current.classifier.pkl'
    print("Storing classifier as " + filename)
    #_ = joblib.dump(classifier, filename)
    with open(filename, 'wb') as f:
        _ = pickle.dump(classifier, f)



    return

    ##################
    # LOAD CLASSIFIER
    ##################

    #classifier = joblib.load(filename)

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
    fails_log += "LOG: ALL INCORRECTLY PREDICTED EMAILS\n"

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
            fails_log += '\n' + print_sample(test)

    with open('fails.log', 'wb') as f:
        f.write(fails_log.encode())

    precision = num_correct / num_predicted_scam
    recall = num_correct / num_labeled_scam
    f_score = 2*precision*recall/(precision+recall)

    print("\nWith a corpus of " + str(num_scam) + " Scam emails and " + str(num_non_scam) + " Non-Scam emails")
    print("After Training with " + str(len(train_data)) + " emails and Testing with " + str(len(test_data)) + " emails")
    print("Emails were correctly classified with: \n")
    print("Precision: {:.2%} ".format(precision))
    print("Recall:    {:.2%} ".format(recall))
    print("F-Score:   {:.2%} ".format(f_score))

    ################################
    # TEST AGAINST RANDOM EMAIL SET
    ################################

    # print("\nRunning against unlabeled dataset")
    # with open("dataset/All_mail-001.mbox", encoding='latin-1') as f:
    #     examples = f.read().splitlines()
    #
    # raw_test_emails = parse_mbox(examples)
    # test_emails = []
    #
    # for em in raw_test_emails:
    #     test_emails.append({'email_body_text': em, 'label': 0})
    #
    # print(len(test_emails))
    # print(test_emails[0])
    # print(test_emails[1])
    #
    # print("\nStripping HTML from EMails, Converting to Lower Case for Comparisons (This may take a few minutes)")
    # for em in test_emails:
    #     em['email_body_processed'] = strip_html(em['email_body_text']).lower()
    #
    # print("Stripping Non-Words from the EMail Bodies")
    # strip_non_words(test_emails)
    #
    # print("\nRunning Classifier and Logging Scam Predictions")
    # scam_log = ''
    # scam_log += "LOG: ALL MAIL PREDICTED AS SCAM\n"
    #
    # for test in test_emails:
    #     vector_data = vectorizer.transform([test['email_body_processed']])
    #     result = classifier.predict(vector_data)[0]
    #     test['prediction'] = result
    #     if result == 1:
    #         scam_log += '\n' + print_sample(test)
    #
    # with open('scams.log', 'wb') as f:
    #     f.write(scam_log.encode())


if __name__ == "__main__":
    main()
