import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from nltk.tokenize import word_tokenize
import re

class Label_Data:
    def __init__(self, file):
        self.file = file

    def sentiment_scores(self, sentence):
        """
            Return a sentiment score for a sentence.

            Parameters
            ----------
            sentence: string
                sentence to be analyzed

            Returns
            -------
            int
                sentiment score
        """
        analyzer = SentimentIntensityAnalyzer()
        sentiment_dict = analyzer.polarity_scores(sentence)

        if sentiment_dict['compound'] >= 0.05:
            return 1
        elif sentiment_dict['compound'] <= - 0.05:
            return -1
        else:
            return 0

    def create_path(self):
        """
            Create a path for the labeled data.

            Returns
            -------
            string
                path to the labeled data
        """
        res = re.findall(r'(\d+)', self.file)
        return f'Data\YouTubeCommentsLabeled{res[0]}.csv'

    def label_data(self):
        """
            Write the labeled data to a csv file.
        """
        labeled = []

        with open(self.file, mode='r', encoding='utf-8') as comment_file:
            for line in comment_file:
                labeled.append([line, self.sentiment_scores(line)])

        columns = ['comment_text', 'sentiment']
        com_lab = pd.DataFrame(labeled, columns=columns)

        com_lab.to_csv(self.create_path())

if __name__ == "__main__":
    test = Label_Data('Smaller Files\end_line_10000.txt')
    test.label_data()
