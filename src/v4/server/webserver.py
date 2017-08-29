from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from src.v4.server import settings
import time
import json


app = Flask(__name__)
app.config.from_object('src.v4.server.settings')
socketio = SocketIO(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/msg', methods=['POST'])
def msg():
    data = request.get_json()
    if 'text' not in data or 'user' not in data:
        return json.dumps({'error': 'text or user missing'}), 400, {'ContentType': 'application/json'}
    send_msg(data['text'], data['user'], data.get('style',''), data.get('attachment',''))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@socketio.on('connect')
def client_connect():
    # emit('my_response', {'data': 'Connected', 'count': 0}, broadcast=True)
    # some test chat messages
    print('s1')
    send_msg('hello', 'mozart')
    time.sleep(2)
    print('s2')
    send_msg("what's up buddy?", 'kant')
    time.sleep(2)
    print('s3')
    send_msg("Where is the logic", 'mozart')


def send_msg(text, user, style='', attachment=''):
    print('send_msg')
    socketio.emit('msg', {
        'text': text,
        'user': user,
        'style': style,
        'attachment': attachment
    }, broadcast=True)


def launch():
    # print('starting webserver: http://localhost:'+ str(settings.PORT))
    socketio.run(app, host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)

# RUN APP
if __name__ == "__main__":
    launch()
