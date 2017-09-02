from flask import Flask, render_template, request
from flask_socketio import SocketIO
import settings
import json

# "threading", "eventlet" or "gevent"
async_mode = 'threading'
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/msg', methods=['POST'])
def msg():
    data = request.get_json()
    if 'text' not in data or 'user' not in data:
        return json.dumps({'error': 'text or user missing'}), 400, {'ContentType': 'application/json'}
    send_msg(data['text'], data['user'], data.get('style',''), data.get('attachment',''))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@socketio.on('connect')
def client_connect():
    send_msg('hello', 'connected')


def send_msg(text, user, style='', attachment=''):
    # print('send_msg')
    socketio.emit('msg', {
        'text': text,
        'user': user,
        'style': style,
        'attachment': attachment
    }, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
