import pydle
import markov

import argparse
import sys
import os
import random
import time

# this contemporary celebration of doing-things-for-yourself in all aspects of life from politics to music
# the end of a fixed potential


class EcoIrcClient(pydle.Client):
    def set_markov(self, name, markov):
        print('loading ' + name)

        self.name = name
        self.markov = markov

    def on_connect(self):
        super().on_connect()
        self.join('#eco')

    def on_private_message(self, by, message):
        super().on_private_message(by, message)
        self.message(by, 'Fuck off.')

    def get_random_sequence(self, message, length):
        split_msg = message.split()
        start_index = 0
        if len(split_msg) > length + 1:
            start_index = random.randint(0, len(split_msg) - (length + 1))
        return ' '.join(split_msg[start_index:start_index+length])

    def get_best_score(self, scores):
        scores.sort(key=lambda scores: scores[1], reverse=True)
        return scores[0]

    def on_message(self, target, by, message):
        super().on_message(target, by, message)

        if (self.name + ' ') in message:
            message = message.replace(self.name, '')

            scores = []
            for i in range(100):
                sequence = self.get_random_sequence(message, 3)
                score = self.markov.score_for_line(sequence.split())
                scores.append((sequence, score))
            best = self.get_best_score(scores)

            # get a random user from the channel to talk to
            users_in_channel = self.channels['#eco']['users']
            users_in_channel.remove(self.name)
            next_bot = random.choice(tuple(users_in_channel))
            if best[1] > 30:
                answer = ' '.join(self.markov.generate(seed=best[0].split(), max_words=100))
            else:
                answer = ' '.join(self.markov.generate(max_words=100))
            answer = next_bot + ' ' + answer
            print(self.name + ' will interpret the message. best score for sentence: ', best)
            print('new answer: ' + answer)
            time.sleep(15)
            self.message(target, answer)

def process_arguments(args):
    parser = argparse.ArgumentParser(description='configure the irc clients')

    parser.add_argument('--txts_path', action='store', help='path to folder with txt files')
    params = vars(parser.parse_args(args))

    return params

def get_authors_list():
    authors = []
    for file in os.listdir(txts_path):
        if not file.endswith('.txt'):
            continue
        author = file.partition('-')[0]
        if author in authors:
            author += '_'
        authors.append(author)
    return authors

from threading import Thread

class MarkovCalculator(Thread):
    def __init__(self, lines, author):
        self.lines = lines
        self.author = author
        super(MarkovCalculator, self).__init__()

    def run(self):
        self.markov_chain = markov.Markov(prefix=self.author)

        for s in self.lines:
            print('trainging ' + self.author + ' with line ' + s)
            self.markov_chain.add_line_to_index(s.split())


if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])
    txts_path = params['txts_path']

    count = 0
    pool = pydle.ClientPool()
    processes = []
    for file in os.listdir(txts_path):
        if not file.endswith('.txt') or count >= 10:
            continue

        path = txts_path + file

        f = open(path, 'r')
        print('opened ' + path)
        line_count = 0
        lines = []
        for line in f:
            line_count += 1
            lines.append(line)

        author = file.partition('-')[0]

        p = MarkovCalculator(lines, author)
        p.start()
        processes.append(p)

        count += 1

    for p in processes:
        p.join()

    for p in processes:
        client = EcoIrcClient(p.markov_chain.prefix)
        client.set_markov(p.markov_chain.prefix, p.markov_chain)
        client.connect('irc.schwittlick.net', tls=False)
        pool.add(client)

    pool.handle_forever()
