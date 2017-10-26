import requests
import json


def ask(text=None):
    resp = requests.post("http://localhost:9000/quest",None,{"text": text} if text else None)
    resp.encoding = "UTF-8"
    print(json.dumps(json.loads(resp.text)['fortune'], indent=2))
    return json.loads(resp.text)['fortune'][0].strip()

print(ask())
print(ask("love sex"))
