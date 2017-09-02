import requests
import json
import time

from state.postmanager import PostManager

if __name__ == "__main__":
    postmanager = PostManager()
    while True:
        postmanager.add()
        time.sleep(1)
        last = postmanager.last()
        json_to_send = json.dumps\
        (
            {
            "text": last.dict()['textRepresentation'],
            "user": last.dict()['text'],
            "style": last.dict()['style'],
            "timestamp": last.dict()['timestamp'],
            "attachment": ""
            }
        )
        result = requests.post('http://localhost:8090/msg', json_to_send, headers={'Content-Type': 'application/json'})
        print(result)