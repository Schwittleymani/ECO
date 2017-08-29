import requests
import json

if __name__ == "__main__":
    result = requests.post('http://localhost:8090/msg', json.dumps({
        "text": "some bla",
        "user": "cunt",
        "style": "",
        "attachment": ""}),
       headers={'Content-Type': 'application/json'})
    print(result)