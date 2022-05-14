import string
import contractions
import pandas as pd
import numpy as np
import time

from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from Preprocess import Cleaner

class Train_and_Predict:

    def __init__(self, file):
        self.data = pd.read_csv(file, encoding='utf-8', on_bad_lines='skip')
        self.punc = string.punctuation
        self.language = English()
        self.stopwords = list(STOP_WORDS)

        self.vectorizer = TfidfVectorizer(max_features=2500, min_df=7, max_df=0.8, stop_words=self.stopwords)
        self.classifier = RandomForestClassifier(n_estimators=200, random_state=0)

        self.start_time = None
        self.end_time = None
        self.elapsed_time = None

        self.sets = self.split_data()

    def preprocess(self, comment_list):
        self.start_time = time.time()

        cleaner = Cleaner()
        for idx, sentence in enumerate(comment_list):
            sentence = cleaner.remove_digits(sentence)
            sentence = cleaner.to_lowercase(sentence)
            sentence = cleaner.remove_newlines(sentence)
            sentence = cleaner.remove_extra_spaces(sentence)
            sentence = cleaner.remove_lead_trail_space(sentence)

            comment_list[idx] = sentence

        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

        return comment_list

    def split_data(self):
        comments = self.data['comment_text'].values
        sentiments = self.data['sentiment'].values

        comments = self.preprocess(comments)

        comments = self.vectorize(comments)

        # split into x_train, x_test, y_train, y_test
        return train_test_split(comments, sentiments, test_size=0.2, random_state=1000) 

    def vectorize(self, comments):
        return self.vectorizer.fit_transform(comments)

    def train(self):
        self.classifier.fit(self.sets[0], self.sets[2])

    def predict(self):
        pred = self.classifier.predict(self.sets[1])

        #print(confusion_matrix(self.sets[3], pred))
        print(classification_report(self.sets[3], pred))
        print(f'The accuracy of the model is {accuracy_score(self.sets[3], pred)}')

    def new_data(self, file):
        #https://www.reddit.com/r/learnmachinelearning/comments/qnmuv8/x_has_1639_features_but_decisiontreeclassifier_is/
        new_data = []
        
        with open(file, mode='r', encoding='utf-8') as comment_file:
            for line in comment_file:
                new_data.append(line[:-1])

        new_data = self.vectorizer.transform(new_data)
        new_pre = self.classifier.predict(new_data)
        
        return new_pre

    def calculate_sentiment(self, analyzed):
        pos = np.count_nonzero(analyzed == 1)
        neu = np.count_nonzero(analyzed == 0)
        neg = np.count_nonzero(analyzed == -1)
        summed = pos + neu + neg

        per_pos = (pos / summed) * 100
        per_neu = (neu / summed) * 100
        per_neg = (neg / summed) * 100

        print(f'The video\'s comments are {per_pos:.2f}% positive, {per_neu:.2f}% neutral, and {per_neg:.2f}% negative.')

if __name__ == '__main__':
    test = Train_and_Predict('Data\YouTubeCommentsLabeled10000.csv')
    one = time.time()
    test.train()
    test.predict()
    print(f'To classify a new comment, it took {time.time() - one:.2f} seconds.')
    print(f'The average document processing time is {test.elapsed_time:.2f} seconds.')
    #new = test.new_data('Data\Videos\YouTubeCommentList5Hxr9k5Vdc4.txt')
    #new = test.new_data('Data\Videos\YouTubeCommentListYbJOTdZBX1g.txt')
    new = test.new_data('Data\Videos\YouTubeCommentListaR3cw7jGRvI.txt')
    test.calculate_sentiment(new)