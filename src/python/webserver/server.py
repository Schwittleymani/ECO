from flask import Flask, render_template, send_file, safe_join, request,jsonify
from threading import Thread
from flask_socketio import SocketIO

import settings
from StandardAnswers import get_answer

import http_calls

app = Flask(__name__)
app.config.from_object('settings')
socketio = SocketIO(app)



@app.route('/', methods=['GET', "POST"])
def index():
    # grammar test
    text = request.args.get('preProc')
    print text
    if text:
        return http_calls.text_preproccess(text)
    else:
        return render_template('index.html')

@app.route('/inter', methods=['GET'])
def interception():
    return render_template('inter.html')


@app.route('/input', methods=["POST"])
def input():
    http_calls.input()



@socketio.on('key')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

def launch():
    def start_websocket_server():

        socketio.run(app, port=app.config['PORT_WEBSOCKET'])
    #Thread(target=start_websocket_server).start()
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])

    #logger.debug("Application terminates")

# RUN APP
if __name__ == "__main__":
    launch()
