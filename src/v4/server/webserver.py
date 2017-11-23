from flask import Flask, render_template, request
from flask_socketio import SocketIO
import settings
import json
import datetime
import os

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

    if settings.RECORD:
        recording_file.write(json.dumps(data) + '\n')
        recording_file.flush()

    if 'text' not in data or 'user' not in data:
        return json.dumps({'error': 'text or user missing'}), 400, {'ContentType': 'application/json'}
    send_msg(data, bcast=True)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@socketio.on('connect')
def client_connect():
    sessid = request.sid
    #send_msg({"timestamp": "from the future", "style": "unformatted", "attachment": None, "text": "welcome " + str(sessid), "user": "eco"})


def send_msg(data, bcast=False):
    socketio.emit('msg', data, broadcast=bcast)

if __name__ == "__main__":
    if settings.RECORD:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        if not os.path.isdir:
            os.makedirs('logs')
        recording_file = open('logs/' + str(timestamp) + '.json', 'w')

    socketio.run(app, host=settings.HOST, port=settings.PORT, debug=settings.DEBUG ) # add ssl_context='adhoc' for https
