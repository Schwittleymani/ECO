from flask import Flask, render_template, send_file, safe_join, request,jsonify
from threading import Thread
from flask_socketio import SocketIO

import http_calls
import settings
from StandardAnswers import get_answer


app = Flask(__name__)
app.config.from_object('webserver.settings')
socketio = SocketIO(app)


'''
not crazy robust so I'll leave the issue open.
the ml thread is not killed.
you don't just kill threads in python...
... how to behave when another input is sent...

also fails and sents status 400 when sent data does not contain 'inputS'


'''
def set_generator(generator):
    http_calls.set_generator(generator)

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
    print request.data
    text = request.json['inputS']
    return http_calls.input(text)



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
