import requests
import time
import random
import argparse
import sys


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
        json_to_send = postmanager.last().json()
        print('sent: ' + json_to_send)
        result = requests.post('http://localhost:8090/msg', json_to_send, headers={'Content-Type': 'application/json'})
        if not result.ok:
            print(result.__dict__)

        if isinstance(post, InteractivePost):
            time.sleep(7)
        else:
            time.sleep(random.uniform(1, 4))


if __name__ == "__main__":
    params = process_arguments(sys.argv[1:])

    replay_path = params['replay']

    if replay_path:
        replay_lines = []
        replay_file = open(replay_path, 'r')
        for line in replay_file.readlines():
            replay_lines.append(line)
        replay_file.close()

        while True:
            for line in replay_lines:
                print('sending: ' + line)
                result = requests.post('http://localhost:8090/msg', line, headers={'Content-Type': 'application/json'})
                if not result.ok:
                    print(result.__dict__)

                time.sleep(random.uniform(1, 4))
    else:
        run_live()
