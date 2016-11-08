import pydle
import markov

import threading
import argparse
import sys
import os
import random
import time

# this contemporary celebration of doing-things-for-yourself in all aspects of life from politics to music
# the end of a fixed potential


class EcoIrcClient(pydle.Client):

    SEQUENCE_MATCH_LENGTH = 3
    MAX_GENERATOR_LENGTH_CHARACTERS = 100
    SIMILARITY_THRESHOLD_PERCENTAGE = 2 # 0-100
    OWNERS_NAME = ['mrzl', 'ra']
    ANSWER_DELAY_SECONDS = 15
    CHANNEL = '#eco'

    last_message = ()

    def set_markov(self, name, markov):
        print('Starting IRC Client of ' + name)
        self.name = name
        self.markov = markov

    def on_connect(self):
        super().on_connect()
        self.join('#eco')

    def on_notice(self, target, by, message):
        super().on_notice(target, by, message)

        if message == 'your turn':
            print(target, by, message)
            time.sleep(2)
            self.write_to_channel('#eco')

    def on_private_message(self, by, message):
        super().on_private_message(by, message)
        self.message(by, 'Fuck off.')

    def get_random_sequence(self, input, length=3):
        """
        generates a random sub-string from the passed input string. with a given length.
        """
        split_msg = input.split()
        start_index = 0
        if len(split_msg) > length + 1:
            start_index = random.randint(0, len(split_msg) - (length + 1))
        return ' '.join(split_msg[start_index:start_index+length])

    def get_best_score(self, scores):
        """
        calculates the best score of a passed tuple list. it contains (string, score)
        """
        # sorting reversed by second elements of the tuple list.
        scores.sort(key=lambda scores: scores[1], reverse=True)
        # maximum is at first index
        return scores[0]

    def on_message(self, target, by, message):
        """
        called when a new message is posted in the channel
        """
        super().on_message(target, by, message)
        self.last_message = (target, message)

    def write_to_channel(self, channel):
        scores = []
        attempt_count = 100
        for i in range(attempt_count):
            # gets a new random sequence from the message
            sequence = self.get_random_sequence(self.last_message[1], self.SEQUENCE_MATCH_LENGTH)
            # calculates the score, of how likely this was generated from this bot
            score = self.markov.score_for_line(sequence.split())
            # stores sequence and score for calculating the best result
            scores.append((sequence, score))
        # calculates the best result contains (sequence, score)
        best = self.get_best_score(scores)

        users = self.channels[channel]['users']
        if self.name in users:
            users.remove(self.name)
        for owner in self.OWNERS_NAME:
            if owner in users:
                users.remove(owner)

        # get a random user from the channel to talk to
        next_bot = random.choice(tuple(users))
        # check if the best answer score is above some certain threshold
        best_score = best[1]
        if best_score > self.SIMILARITY_THRESHOLD_PERCENTAGE:
            # if it is above some threshold, generate a message with that sequence as seed
            answer = ' '.join(self.markov.generate(seed=best[0].split(), max_words=self.MAX_GENERATOR_LENGTH_CHARACTERS))
        else:
            # if is is below, generate a completely new message
            answer = ' '.join(self.markov.generate(max_words=self.MAX_GENERATOR_LENGTH_CHARACTERS))

        #answer = next_bot + ' ' + answer
        print(self.name + ' will interpret the message. best score for sentence: ', best)
        print('new answer: ' + answer)
        time.sleep(self.ANSWER_DELAY_SECONDS)
        self.message(channel, answer)
        time.sleep(1)
        self.notice(next_bot, 'your turn')


class MarkovCalculator(threading.Thread):
    def __init__(self, lines, author):
        self.lines = lines
        self.author = author
        super(MarkovCalculator, self).__init__()

    def run(self):
        self.markov_chain = markov.Markov(prefix=self.author)

        print('Start training ' + self.author)
        for s in self.lines:
            #print('trainging ' + self.author + ' with line ' + s)
            self.markov_chain.add_line_to_index(s.split())
        print('Done training ' + self.author)


def process_arguments(args):
    parser = argparse.ArgumentParser(description='configure the irc clients')

    parser.add_argument('--txts_path', action='store', help='path to folder with txt files')
    parser.add_argument('--max_bots', action='store', help='the maximum number of bots to train and connect to IRC')
    params = vars(parser.parse_args(args))

    return params


if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    txts_path = params['txts_path']
    max_bots = int(params['max_bots'])

    count = 0
    processes = []
    authors = []
    for file in os.listdir(txts_path):
        if not file.endswith('.txt') or count >= max_bots:
            continue

        path = txts_path + file

        f = open(path, 'r')
        print('Loaded ' + path)
        line_count = 0
        lines = []
        for line in f:
            line_count += 1
            lines.append(line)

        if line_count < 300:
            continue

        author = file.partition('-')[0]
        author = author[:15]
        author.replace('.', '')
        if author in authors:
            author += '_'
        authors.append(author)

        p = MarkovCalculator(lines, author)
        p.start()
        processes.append(p)

        count += 1

    for p in processes:
        p.join()

    pool = pydle.ClientPool()
    for p in processes:
        client = EcoIrcClient(p.markov_chain.prefix)
        client.set_markov(p.markov_chain.prefix, p.markov_chain)
        client.connect('irc.schwittlick.net', tls=False)
        pool.add(client)

    print('Setup done.')
    pool.handle_forever()
