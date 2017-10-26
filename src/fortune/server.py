from flask import Flask, render_template, request
import json

import model
#,template_folder='src/fortune/templates'
app = Flask(__name__)

HOST = '0.0.0.0'
PORT = 9000
DEBUG = False


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/quest', methods=['GET', 'POST'])
def msg():
    data = request.get_json()
    text = data['text']
    mode = data['mode']
    print(text, mode)

    if text:
        if mode == '':
            result = model.sort_emotional_valence(text)
        else:
            result = model.model.get_top_n(text)
        result = json.dumps({'fortune': result}), 200, {'ContentType': 'application/json'}
    else:
        result = json.dumps({'fortune': [model.model.select_random().strip()]}), 200, {'ContentType': 'application/json'}
    return result #render_template('index.html')

def launch():
    app.run(host=HOST, port=PORT, debug=True)
