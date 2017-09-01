import requests
import json
import time

from state.postmanager import PostManager

if __name__ == "__main__":
    postmanager = PostManager()
    while True:
        postmanager.add()
        time.sleep(2)
        last = postmanager.last()
        result = requests.post('http://localhost:8090/msg', json.dumps({
            "text": last.dict()['textRepresentation'],
            "user": last.dict()['text'],
            "style": last.dict()['style'],
            "attachment": ""}),
           headers={'Content-Type': 'application/json'})
        if not result.ok:
            print(result.error)
