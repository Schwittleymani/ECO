import requests
import json
import time

from state.postmanager import PostManager
from state.postmanager import PostType

if __name__ == "__main__":
    postmanager = PostManager()
    while True:
        postmanager.add(PostType.POST_TYPE_KAOMOJI)
        time.sleep(1)
        result = requests.post('http://localhost:8090/msg', json.dumps({
            "text": postmanager.last().text(),
            "user": "cunt",
            "style": "",
            "attachment": ""}),
           headers={'Content-Type': 'application/json'})
        print(result)