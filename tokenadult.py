
import pickle
import random
import re
import string

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

    def generate_corpus(self, data):
        w1 = self.stop
        w2 = self.stop
        for line in data:
            line = self.sanitize(line)
            #print line
            for word in line.split():
                # add word without punctuation
                if word[-1] in self.end_sentence:
                    self.corpus.setdefault((w1, w2), []).append(word[0:-1]) 
                    w1, w2 = w2, word[0: -1]
                    word = word[-1]
                self.corpus.setdefault((w1, w2), []).append(word)
                w1, w2 = w2, word
        self.corpus.setdefault((w1, w2), []).append(self.stop)

    # seed should be a bigram separated by a space
    # ie: "I wish"
    def generate_response(self, seed):
        response = []
        key = seed

        for x in range(self.max_words):

            words = key.split()
            words = map(self.sanitize, words)

            response.append(words[0])

            new_word = random.choice(self.corpus[(words[0], words[1])])

            if not new_word:
                break

            key = words[1] + " " + new_word

        for i in range(len(response)):
            if response[i - 1] and response[i - 1] == ".":
                response[i] = string.capwords(response[i])

        response[0] = string.capwords(response[0])
        response[-1] += '.'

        str_response = ' '.join(response)

        return re.sub(r'\s([?.!"](?:\s|$))', r'\1', str_response)

    def load(self, filename):
        with open(filename, "rb") as f:
            try:
                self.corpus = pickle.load(f)
                print("Pickle load was successful.")
                return True
            except:
                print("Loading corpus failed.")
                return False

    def dump(self, filename):
        try:
            with open(filename, "wb") as f:
                pickle.dump(self.corpus, f)
                print("Pickle dump was successful.")
                return True
        except:
            print("Could not dump.")
            return False

if __name__ == "__main__":
    ta = MarkovTokenAdult()
    # string = """
    # Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed at auctor metus. Vestibulum ullamcorper mi id eleifend tincidunt. Donec volutpat lectus tortor, eget dictum nunc ultricies eget. In tempus malesuada metus, eu tempor mi sagittis ut. Quisque eu purus nec odio sollicitudin pharetra sit amet in nunc. Ut eget nulla elit. Maecenas consectetur, turpis ut egestas aliquet, purus nunc cursus orci, sed laoreet orci lorem non magna.
    # Mauris pretium risus vel ligula pretium facilisis. Praesent at hendrerit massa. Sed eget tellus non ipsum ullamcorper venenatis. Phasellus et lacus sed nisl aliquam fringilla. Sed id eros id libero luctus dictum. Donec eleifend magna turpis, at venenatis mi ultricies at. Aliquam commodo, enim ac dignissim pretium, libero risus euismod libero, eu porttitor orci nunc congue mauris. Donec nulla ligula, imperdiet non rhoncus eget, feugiat non libero. Donec in purus nec nunc imperdiet vehicula vel ut ligula. Sed feugiat consequat odio, sed lobortis orci suscipit sit amet. Donec quis suscipit diam.
    # Morbi non tellus tristique, vestibulum odio id, sollicitudin arcu. Praesent egestas, lectus ac tristique feugiat, metus lectus iaculis magna, quis pharetra urna diam ut lacus. Integer laoreet a enim id tristique. Proin sed eros ac libero consequat volutpat. Ut molestie hendrerit rutrum. Suspendisse potenti. Nulla facilisi. Sed sit amet metus eget felis venenatis sagittis. Pellentesque molestie vel nisi consequat dictum. Mauris purus neque, lobortis vestibulum purus ut, malesuada facilisis ipsum. Nam porttitor, lectus id dictum fermentum, neque dui ultrices elit, tempor rhoncus mauris lorem vel neque. Aenean felis mi, rhoncus at lectus non, sagittis elementum quam. In posuere mollis diam, sit amet suscipit neque.
    # Pellentesque vehicula augue eget turpis dictum, vel scelerisque purus consequat. Sed eu justo gravida erat dignissim sodales. Nunc id lacus vel nulla congue tempus sit amet lacinia leo. Fusce tempus mi sit amet sollicitudin bibendum. Morbi fringilla libero et laoreet laoreet. Praesent eleifend, arcu at placerat mattis, metus sem pulvinar augue, a tincidunt mi risus sed dolor. Sed tristique urna a ligula condimentum congue. Nam elementum purus velit, ac hendrerit eros mollis quis. Phasellus purus tellus, fermentum non turpis ut, porta lacinia neque. Aliquam in mauris sit amet risus tincidunt vehicula a vel nunc.
    # Duis convallis mauris sed lacus mattis, vitae venenatis velit varius. Suspendisse suscipit arcu sodales porta faucibus. Praesent rutrum ut ante id euismod. Pellentesque eleifend rutrum sapien, sodales feugiat sapien dapibus sit amet. In tellus elit, blandit eu sagittis id, pulvinar id orci. Praesent ultricies est et arcu imperdiet, sit amet convallis eros blandit. Vestibulum mattis, nisl a aliquam facilisis, quam ante rutrum quam, sed pretium orci lectus id diam. Quisque imperdiet tortor quis ultrices ullamcorper. Nunc justo nisi, tristique ut arcu eleifend, vulputate eleifend magna. Curabitur auctor molestie posuere. Pellentesque eu adipiscing est, eget semper dui.
    # """

    #string = string.split('\n')
    #for line in string:
    #   print line
    #ta.generate_corpus(string)
    #print ta.corpus
    ta.load("corpus.p")
    print ta.generate_response("dolor sit")

    #ta.dump("corpus.p")

