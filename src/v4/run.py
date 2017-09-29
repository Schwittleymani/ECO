import requests
import time
import random

from posts.postmanager import PostManager

if __name__ == "__main__":
    postmanager = PostManager()
    while True:
        postmanager.add_random()
        json_to_send = postmanager.last().json()
        print('sent: ' + json_to_send)
        result = requests.post('http://localhost:8090/msg', json_to_send, headers={'Content-Type': 'application/json'})
        if not result.ok:
            print(result.__dict__)
        time.sleep(random.uniform(2, 4))
