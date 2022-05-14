import contractions
import re

class Cleaner:

    def expand_contractions(self, comment):
        """
        Expand all contractions in a sentence
        """
        return contractions.fix(comment)

    def remove_digits(self, comment):
        """
        Remove words with digits
        """
        return re.sub(r'\w*\d\w*', ' ', comment)

    def remove_URLs(self, comment):
        """
        Remove URLs
        https://www.codegrepper.com/code-examples/python/remove+urls+from+text+python
        """
        return re.sub(r'http\S+', ' ', comment)

    def remove_extra_spaces(self, comment):
        """
        Remove double spaces
        """
        return re.sub('\s+', ' ', comment)
    
    def remove_lead_trail_space(self, comment):
        """
        Remove leading and trailing spaces
        """
        return comment.strip()

    def to_lowercase(self, comment):
        """
        All text is to lowercase
        """
        return comment.lower()

    def remove_newlines(self, comment):
        """
        Remove newlines
        """
        return comment.replace('\n', ' ')

    def lemmatize(self, comment):
        """
        Will return the lemmatization and tokenization
        https://medium.com/mlearning-ai/nlp-tokenization-stemming-lemmatization-and-part-of-speech-tagging-9088ac068768
        """
        comment_split = comment.split()
        tokens = [English(word) for word in comment_split]
        return " ".join([token.lemma_.lower().strip() for token in tokens])
