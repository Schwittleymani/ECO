import requests
import json
import time

from state.postmanager import PostManager

if __name__ == "__main__":
    postmanager = PostManager()
    while True:
        postmanager.add()

        last = postmanager.last()
        # TODO so here we gonna add last.to_json() ok?
        json_to_send = json.dumps(
            {
            "text": last.dict()['textRepresentation'],
            "user": last.dict()['text'],
            "style": last.dict()['style'],
            "timestamp": last.dict()['timestamp'],
            "attachment": "",
            }
        )
        print(json_to_send, type(json_to_send))
        result = requests.post('http://localhost:8090/msg', json_to_send, headers={'Content-Type': 'application/json'})
        if not result.ok:
            print(result.__dict__)
        time.sleep(2)