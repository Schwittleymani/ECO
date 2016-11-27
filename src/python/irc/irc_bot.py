import random
import sys
import os
import time
import markov_python3
import pydle
import collections
import argparse

class EcoStatistics(pydle.Client):
    def on_connect(self):
        super().on_connect()
        self.join('#eco')
        self.markov_used = 0
        self.original_used = 0

    def on_private_message(self, by, message):
        super().on_private_message(by, message)
        if 'markov' in message:
            self.markov_used += 1
        elif 'original' in message:
            self.original_used += 1
        elif '--statistic' in message:
            answer = 'Markov: ' + str(self.markov_used) + ' Original: ' + str(self.original_used)
            self.message(by, answer)

class MarkovAnswerGenerator(object):

    SEQUENCE_MATCH_LENGTH = 3
    MAX_GENERATOR_LENGTH_CHARACTERS = 100
    SIMILARITY_THRESHOLD_PERCENTAGE = 2 # 0-100
    KEYWORD_ORIGINAL_USED = 'original'
    KEYWORD_MARKOV_USED = 'markov'

    markov_used = 0
    original_used = 0

    def __init__(self, markov):
        self.markov = markov

    def generate_answer(self, best_result_string, best_result_score):
        if best_result_score > self.SIMILARITY_THRESHOLD_PERCENTAGE:
            # if it is above some threshold, generate a message with that sequence as seed
            answer = ' '.join(self.markov.generate(seed=best_result_string.split(), max_words=self.MAX_GENERATOR_LENGTH_CHARACTERS))
            # if the generated answer is the same as the best possible answer.
            if answer == best_result_string:
                answer = self.get_original_sentence(best_result_string=best_result_string)
                technique_used = self.KEYWORD_ORIGINAL_USED
                self.original_used += 1
            else:
                technique_used = self.KEYWORD_MARKOV_USED
                self.markov_used += 1
        else:
            # if is is below, generate a completely new message
            answer = self.get_original_sentence(best_result_string=best_result_string)
            technique_used = self.KEYWORD_ORIGINAL_USED
            self.original_used += 1

        return answer, technique_used

    def get_original_sentence(self, best_result_string=''):
        answer = ''
        for _line in self.markov.lines:
            if best_result_string in ' '.join(_line):
                answer = ' '.join(_line)
        if answer == '':
            answer = random.choice(self.markov.lines)
        return answer

    def get_random_sequence(self, input, length=3):
        """
        generates a random sub-string from the passed input string. with a given length.
        """
        split_msg = input.split()
        random.shuffle(split_msg)
        start_index = 0
        if len(split_msg) > length + 1:
            start_index = random.randint(0, len(split_msg) - (length + 1))
        return ' '.join(split_msg[start_index:start_index+length])

    def calc_best_score(self, last_message):
        scores = []
        attempt_count = 200
        for i in range(attempt_count):
            # gets a new random sequence from the message
            sequence = self.get_random_sequence(last_message, self.SEQUENCE_MATCH_LENGTH)
            # calculates the score, of how likely this was generated from this bot
            score = self.markov.score_for_line(sequence.split())
            # stores sequence and score for calculating the best result
            scores.append((sequence, score))

        # calculates the best result contains (sequence, score)
        scores.sort(key=lambda scores: scores[1], reverse=True)
        return scores[0]

    def compose_message(self, last):
        # check if the best answer score is above some certain threshold
        best = self.calc_best_score(last_message=last)
        best_result_string = best[0]
        best_result_score = best[1]
        answer = self.generate_answer(best_result_score=best_result_score, best_result_string=best_result_string)

        return answer


class EcoIrcClient(pydle.Client):

    STATISTIC_BOT = 'HumammadSusej'
    OWNERS_NAME = ['mrzl', 'marmar', 'ra', STATISTIC_BOT]
    ANSWER_DELAY_SECONDS = 2
    CHANNEL = '#eco'
    KEYWORD_TURN = 'your turn'

    corpus_name = None
    last_channel_message = None
    last_messages = collections.deque(maxlen=100)

    def __init__(self, prefix, markov, corpus_name):
        super().__init__(prefix)

        self.generator = MarkovAnswerGenerator(markov)
        self.name = markov.prefix
        self.corpus_name = corpus_name

        self.last_channel_message = self.generator.get_original_sentence()

        self.parser = argparse.ArgumentParser(description='configure the irc clients')
        self.parser.add_argument('--statistic', action='store_true', help='returns statistic')
        self.parser.add_argument('--corpus', action='store_true', help='returns the used corpus name')
        self.parser.add_argument('--last', action='store', help='returns the last n messages', type=int)

    def on_connect(self):
        """
        called once the client is connected to the network
        """
        super().on_connect()
        self.join(self.CHANNEL)

    def on_notice(self, target, by, message):
        """
        called when this client has received a /notice *nick* notice_message

        :param target: the own name of this irc client
        :param by: the nick who sent the notice
        :param message: the message attached to the notice
        :return:
        """

        super().on_notice(target, by, message)

        # if the notice contained the commando that indicates it's this clients turn
        if self.KEYWORD_TURN in message:
            # generate an answer
            answer, technique = self.generator.compose_message(self.last_channel_message)

            # a bit of delay
            time.sleep(self.ANSWER_DELAY_SECONDS)

            # sends the new message to the channel
            self.message(self.CHANNEL, answer)

            # saving statistics
            self.statistics(self.CHANNEL, answer, technique)

            # notifies next bot for its turn
            self.notice(self.random_bot(), self.KEYWORD_TURN)

    def on_message(self, target, by, message):
        """
        called when a new message is posted in the channel
        """
        super().on_message(target, by, message)

        # saving last posted channel message
        self.last_channel_message = message

    def parse_private_message(self, by, message):
        """
        parses the message to check if it was a command or just a text for direct conversation
        :param by: which nickname sent the message
        :param message: the content
        :return: True if the message was a command, False if it was not one of the defined commands
        """
        params, unknown = self.parser.parse_known_args(message.split())
        params = vars(params)

        if params['statistic'] is True:
            answer = 'Markov: ' + str(self.generator.markov_used) + ' Original: ' + str(self.generator.original_used)
            self.message(by, answer)
            return True
        if params['corpus'] is True:
            self.message(by, self.corpus_name)
            return True
        if params['last'] is not None and isinstance(params['last'], int):
            amount = max(0, min(params['last'], len(self.last_messages)))
            for i in list(reversed(self.last_messages))[:amount]:
                self.message(by, i)
                time.sleep(0.1)
            return True
        return False

    def on_private_message(self, by, message):
        """
        this is called when a private message was received.
        1. checks if the message was a commando
        2. if not, answer to the message directly

        :param by: who sent the message
        :param message: the content of the message
        :return: nothing
        """
        super().on_private_message(by, message)
        was_command = self.parse_private_message(by, message)
        if not was_command:
            answer, technique = self.generator.compose_message(self.last_channel_message)
            self.message(by, answer)
            self.statistics(by, answer, technique)

    def statistics(self, answer, technique):
        # saving statistics
        self.message(self.STATISTIC_BOT, technique)
        self.last_messages.append(answer)

    def random_bot(self):
        """
        chooses a random conversation partner from the current channel

        :return: nick name of the chosen partner
        """
        users = self.channels[self.CHANNEL]['users']
        if self.name in users:
            users.remove(self.name)
        for owner in self.OWNERS_NAME:
            if owner in users:
                users.remove(owner)

        next_bot = random.choice(tuple(users))
        return next_bot


def process_arguments(args):
    parser = argparse.ArgumentParser(description='configure the irc clients')

    parser.add_argument('--txt_path', action='store', help='the path to the directory containing the file')
    parser.add_argument('--server', action='store', help='the server to connect the bots to', type=str, default='localhost')
    params = vars(parser.parse_args(args))

    return params


if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])

    txt_path = params['txt_path']
    server = params['server']

    file_path, file_name = os.path.split(txt_path)
    lines = open(txt_path, 'r').readlines()

    author = file_name.partition('-')[0]
    markov_chain = markov_python3.Markov(prefix=author)

    for s in lines:
        markov_chain.add_line_to_index(s.split())

    print('Done training ' + author)

    client = EcoIrcClient(author, markov_chain, file_name)
    client.connect(server, tls=False)
    client.handle_forever()