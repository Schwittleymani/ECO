from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
import numpy as np
import pickle
import os

class LSTMWrapper(object):
    def __init__(self, maxlen):
        self.maxlen = maxlen

    def load(self, path):
        text = open(path).read().lower()
        print('corpus length:', len(text))

        self.chars = sorted(list(set(text)))
        print('total chars:', len(self.chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

        # cut the text in semi-redundant sequences of maxlen characters
        step = 3
        sentences = []
        next_chars = []
        for i in range(0, len(text) - self.maxlen, step):
            sentences.append(text[i: i + self.maxlen])
            next_chars.append(text[i + self.maxlen])
        print('nb sequences:', len(sentences))

        print('Vectorization...')
        self.X = np.zeros((len(sentences), self.maxlen, len(self.chars)), dtype=np.bool)
        self.y = np.zeros((len(sentences), len(self.chars)), dtype=np.bool)
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                self.X[i, t, self.char_indices[char]] = 1
                self.y[i, self.char_indices[next_chars[i]]] = 1

        # build the model: a single LSTM
        print('Build model...')
        self.model = Sequential()
        self.model.add(LSTM(128, input_shape=(self.maxlen, len(self.chars))))
        self.model.add(Dense(len(self.chars)))
        self.model.add(Activation('softmax'))

        optimizer = RMSprop(lr=0.01)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    def train(self, iterations, epochs):
        # train the model, output generated text after each iteration
        for iteration in range(1, iterations):
            print('Iteration ' + str(iteration) + ' / ' + str(iterations))
            self.model.fit(self.X, self.y, batch_size=128, nb_epoch=epochs)

    def sample(self, diversity, seed, output_length):
        output_text = seed
        input_text = seed
        for i in range(output_length):
            x = np.zeros((1, self.maxlen, len(self.chars)))
            for t, char in enumerate(input_text):
                x[0, t, self.char_indices[char]] = 1.

            preds = self.model.predict(x, verbose=0)[0]
            next_index = self.__sample_character(preds, diversity)
            next_char = self.indices_char[next_index]

            input_text = input_text[1:] + next_char

            output_text += next_char

        return output_text

    def save_model(self, save_path, filename):
        output_path = save_path + '/' + filename + '.h5'
        print('output_path:' + output_path)
        self.model.save(output_path)

        with open(save_path + '/' + filename + '_chars.pkl', 'wb') as file:
            pickle.dump(self.chars, file, pickle.HIGHEST_PROTOCOL)

        with open(save_path + '/' + filename + '_char_indices.pkl', 'wb') as file:
            pickle.dump(self.char_indices, file, pickle.HIGHEST_PROTOCOL)

        with open(save_path + '/' + filename + '_indices_char.pkl', 'wb') as file:
            pickle.dump(self.indices_char, file, pickle.HIGHEST_PROTOCOL)

    def load_model(self, path, filename):
        print('loading: ' + path + filename)
        self.model = load_model(path + filename)
        print('loading here:')
        print(path + filename[:-3] + '_chars.pkl')
        with open(path + filename[:-3] + '_chars.pkl', 'rb') as file:
            self.chars = pickle.load(file)

        with open(path + filename[:-3] + '_char_indices.pkl', 'rb') as file:
            self.char_indices = pickle.load(file)

        with open(path + filename[:-3] + '_indices_char.pkl', 'rb') as file:
            self.indices_char = pickle.load(file)

    def __sample_character(self, preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)