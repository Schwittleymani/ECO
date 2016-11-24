import argparse
import sys
import os
import subprocess
import shlex
import glob
import irc_bot

def process_arguments(args):
    parser = argparse.ArgumentParser(description='configure the irc clients')

    parser.add_argument('--txts_path', action='store', help='path to folder with txt files')
    parser.add_argument('--bot_script_path', action='store', help='path to the irc_bot.py script')
    parser.add_argument('--server', action='store', help='the server to connect the bots to', type=str, default='localhost')
    parser.add_argument('--max_bots', action='store', help='the maximum number of bots to train', type=int, default=10)

    params = vars(parser.parse_args(args))

    return params

def start_individual_bot_process(script_path, file_path, server):
    python_path = os.popen('which python').read().rstrip()
    line = python_path + ' ' + script_path + ' --txt_path ' + file_path + ' --server ' + server
    subprocess.Popen(shlex.split(line), shell=False)


if __name__ == '__main__':
    params = process_arguments(sys.argv[1:])

    txts_path = params['txts_path']
    max_bots = params['max_bots']
    bot_script_path = params['bot_script_path']
    server = params['server']

    for file in glob.glob(txts_path + '/*.txt')[:max_bots]:
        start_individual_bot_process(script_path=bot_script_path, file_path=file, server=server)

    statistic_client = irc_bot.EcoStatistics('STATISTIC_BOT')
    statistic_client.connect(server, tls=False)
    statistic_client.handle_forever()