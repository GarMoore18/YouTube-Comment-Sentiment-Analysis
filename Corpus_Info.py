import nltk
from nltk.draw.dispersion import dispersion_plot
from spacy.lang.en.stop_words import STOP_WORDS

class Corpus_Information():

    def __init__(self, file):
        self.num_of_docs = 1
        self.corpus = file

        self.data = None
        self.words = None
        self.common = None
        self.no_stops = None

        self.open_corpus()

    def get_num_docs(self):
        print(f'There is a total of {self.num_of_docs} documents.')
        return self.num_of_docs

    def open_corpus(self):
        with open(self.corpus, mode='r', encoding='utf-8') as corpus_file:
            self.data = corpus_file.read()
            self.words = self.data.split()

    def get_words(self):
        return self.words

    def get_num_words(self):  
        return len(self.words)

    def get_num_chars(self):
        return len(self.data)

    def get_averages(self):
        words = self.get_num_words()
        chars = self.get_num_chars()
        print(f"There is an average of {words/self.num_of_docs} words per document.")
        print(f"There is an average of {chars/self.num_of_docs} characters per document.")

    def frequency_distribution(self):
        self.no_stops = [w.lower() for w in self.words if w.lower() not in STOP_WORDS]
        freq_dist = nltk.FreqDist(self.no_stops)
        freq_dist.plot(10)
        self.common = freq_dist.most_common(10)

        for i in range(len(self.common)):
            self.common[i] = self.common[i][0]

    def lexical_dispersion(self):
        dispersion_plot(self.no_stops, self.common)

    def lexical_diversity(self):
        vocab = set(self.get_words())
        print(f'The lexical diversity is {self.get_num_words() / len(vocab)}.')
        return self.get_num_words() / len(vocab)

if __name__=="__main__":
    test = Corpus_Information('Data\YouTubeComment.txt')
    test.frequency_distribution()
    test.lexical_dispersion()
    #test.get_num_docs()
    #test.get_averages()
    #test.lexical_diversity()