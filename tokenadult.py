
import pickle
import random
import re

class MarkovTokenAdult():

    '''
    Markov chain irc bot that uses
    as its corpus the hacker news user
    tokenadult's comments and posts. 

    '''

    def __init__(self, max_words=50):
        self.corpus = {}
        self.end_sentence = (".", "?", "!",)
        self.stop = "\n"
        self.max_words = max_words

    def sanitize(self, text):
        return re.sub('[\"\']', '', text.lower())

    # for loading in the training data
    # serialize data using Pickle
    def generate_corpus(self, data):
        w1 = self.stop
        w2 = self.stop
        for line in data:
            line = self.sanitize(line)
            for word in line.split():
                # add word without punctuation
                if word[-1] in self.end_sentence:
                    self.corpus.setdefault((w1, w2), []).append(word[0:-1]) 
                    w1, w2 = w2, word[0: -1]
                    word = word[-1]
                self.corpus.setdefault((w1, w2), []).append(word)
                w1, w2 = w2, word
        self.corpus.setdefault((w1, w2), []).append(self.stop)
