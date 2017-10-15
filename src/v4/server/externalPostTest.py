import requests
import json

if __name__ == "__main__":

    result = requests.post('http://localhost:8090/msg', json.dumps({
        "text": "fuck &#x1F613;  \ud83c\udd71 \u05d4\u05de\u05d5\u05df \u05d0\u05d4\u05d1\u05d4, \u05db\u05d5\u05e9\u05d9 \ud83d\udcaf\ud83d\udcaf\ud83c\uddee\ud83c\uddf1\ud83c\uddee\ud83c\uddf1\ud83c\uddee\ud83c\uddf1\ud83d\udc7d\ud83d\udc7d\ud83d\udc7d\ud83d",
        "user": "cunt",
        "style": "scroll",
        "timestamp": "what?",
        "attachment": None}),
       headers={'Content-Type': 'application/json'})
    print(result)