import requests
import time
import random

from posts.postmanager import PostManager
from posts.post import InteractivePost

if __name__ == "__main__":
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
