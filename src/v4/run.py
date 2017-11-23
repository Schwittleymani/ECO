import requests
import time
import random
import argparse
import json
import sys


def map(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))


def text_to_wait(text):
    text_length = len(text)
    wait_seconds = map(text_length, 0, 100, 1, 10)
    wait_seconds = min(wait_seconds, 15)
    print('text_length: ' + str(text_length) + ' waiting: ' + str(wait_seconds))
    return wait_seconds


def process_arguments(args):
    parser = argparse.ArgumentParser(description='eco #5')
    parser.add_argument('--replay', action='store', help='the path to the json with to replay a story')

    params = vars(parser.parse_args(args))
    return params


def run_live():
    from posts.postmanager import PostManager
    from posts.post import InteractivePost

    postmanager = PostManager()
    while True:
        post = postmanager.add_random()

        json_to_send = post.json()
        print('sent: ' + json_to_send)
        result = requests.post('http://localhost:8090/msg', json_to_send, headers={'Content-Type': 'application/json'})
        if not result.ok:
            print(result.__dict__)

        if isinstance(post, InteractivePost):
            time.sleep(10)
        else:
            wait_seconds = text_to_wait(post.text())
            time.sleep(wait_seconds)


def run_replay(replay_file_path):
    replay_lines = []
    replay_file = open(replay_file_path, 'r')
    for line in replay_file.readlines():
        replay_lines.append(line)
    replay_file.close()

    while True:
        for line in replay_lines:
            print('sending: ' + line)
            result = requests.post('http://localhost:8090/msg', line, headers={'Content-Type': 'application/json'})
            if not result.ok:
                print(result.__dict__)

            wait_seconds = text_to_wait(json.loads(line)['text'])
            time.sleep(wait_seconds)


if __name__ == "__main__":
    params = process_arguments(sys.argv[1:])

    replay_path = params['replay']

    if replay_path:
        run_replay(replay_path)
    else:
        run_live()
