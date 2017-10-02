import random
import nltk
import pickle
import glob
import os
import codecs
import json

from misc import data_access

class MarkovChainBackOff(object):
    def __init__(self, corpus, n_grams, min_length):
        """
        corpus = list of string text ["speech1", "speech2", ..., "speechn"]
        n_grams = max sequence length
        min_length = minimum number of next words required for back-off scheme
        """
        self.grams = {}
        self.n_grams = n_grams
        self.corpus = []
        self.min_length = min_length

    def add_corpus(self, corpus):
        self.corpus = self.corpus + corpus

    def curpus_size(self):
        return len(self.corpus)

    def start(self):
        self.sequences()

    def tokenizer(self, speech, gram):
        """tokenize speeches in corpus, i.e. split speeches into words"""
        tokenized_speech = nltk.word_tokenize(speech)

        if len(tokenized_speech) < gram:
            pass
        else:
            for i in range(len(tokenized_speech) - gram):
                yield (tokenized_speech[i:i + (gram + 1)])

    def sequences(self):
        """
        create all sequences of length up to n_grams
        along with the pool of next words.
        """
        for gram in range(1, self.n_grams + 1):
            dictionary = {}
            for speech in self.corpus:
                for sequence in self.tokenizer(speech, gram):
                    key_id = tuple(sequence[0:-1])

                    if key_id in dictionary:
                        dictionary[key_id].append(sequence[gram])
                    else:
                        dictionary[key_id] = [sequence[gram]]
            self.grams[gram] = dictionary

    def next_word(self, key_id):
        """returns the next word for an input sequence
        but backs off to shorter sequence if length
        requirement is not met.
        """
        for i in range(len(key_id)):
            try:
                if len(self.grams[len(key_id)][key_id]) >= self.min_length:
                    return random.choice(self.grams[len(key_id)][key_id])
            except KeyError:
                pass
        # if the length requirement isn't met, we shrink the key_id
            if len(key_id) > 1:
                key_id = key_id[1:]
        # when we're down to only a one-word sequence,
        #ignore the requirement
        try:
            return random.choice(self.grams[len(key_id)][key_id])
        except KeyError:
            # key does not exist: should only happen when user enters
            # a sequence whose last word was not in the corpus
            # choose next word at random
            return random.choice(' '.join(self.corpus).split())

    def next_key(self, key_id, res):
        return tuple(key_id[1:]) + tuple([res])

    def generate_markov_text(self, start, size=25):
        """"start is a sentence of at least n_grams words"""
        key_id = tuple(nltk.word_tokenize(start))[ - self.n_grams:]
        gen_words = []
        i = 0
        while i <= size:
            result = self.next_word(key_id)
            key_id = self.next_key(key_id, result)
            gen_words.append(result)
            i += 1
        return start + ' ' + ' '.join(gen_words).replace(' .', '.').replace(' ,', ',')


class MarkovManager(object):
    def __init__(self):
        #self.train()

        self._markovs = {}
        markov_model_folder = data_access.get_model_folder() + 'markov/' + '*.pickle'
        print(markov_model_folder)
        pickle_paths = glob.glob(markov_model_folder)
        print(pickle_paths)
        counter = 0
        for path in pickle_paths:
            if counter < 10:
                print('loading' + path)
                _, filename = os.path.split(path)
                self._markovs[filename[:-6]] = self.load(path)
                counter += 1

    @staticmethod
    def save(markov, pickle_file_name):
        with open(pickle_file_name, 'wb') as f:
            pickle.dump(markov, f)

    @staticmethod
    def load(pickle_file_name):
        with open(pickle_file_name, 'rb') as f:
            markov = pickle.load(f)
            return markov

    def generate_random(self, start_string='', len=30):
        print('start: ' + str(start_string))
        author, markov = random.choice(list(self._markovs.items()))
        return author, markov.generate_markov_text(start=start_string, size=len)

    def read_json_file(self, file_name):
        with codecs.open(file_name, encoding='utf-8') as fin:
            return json.loads(fin.read())

    def train(self):
        json = self.read_json_file(data_access.get_project_folder() + 'src/python/notebooks/log-final.json')
        base_path = json['folder_path']

        authors = {}

        for key in json['file_descriptors']:
            values = json['file_descriptors'][key]
            rel_path = values['rel_path']
            if True:  # rel_path == 'arts_arthistory_aesthetics/' or rel_path == 'own_mixed_collection/':
                file_name = values['file_name']
                author_name = values['author_name']
                abs_path = os.path.join(base_path + rel_path, file_name)
                if author_name not in authors:
                    authors[author_name] = []

                authors[author_name].append(abs_path)

        print(len(authors))
        markovs = []
        for key in authors:
            if len(authors[key]) > 5:
                print(key + ' ' + str(len(authors[key])))
                mark = MarkovChainBackOff([], 2, 2)
                for path in authors[key]:
                    lines = open(path, 'r').readlines()
                    mark.add_corpus(lines)
                    print(len(lines))
                if mark.curpus_size() > 10:
                    mark.start()
                    self.save(mark, key + '.pickle')
                    mark.generate_markov_text('We should', size=25)
                    markovs.append(mark)

if __name__ == "__main__":
    doc = ['This is your first text', 'and here is your second text.']

    # mark = MarkovChainBackOff(2, 2)
    # mark.add_corpus(doc)
    # mark.start()
    # save(mark)
    #mark = load('markov.pickle')
    #mark.generate_markov_text('type a sentence that has at least n_grams words', size=25)

