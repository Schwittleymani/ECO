from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, Namespace, emit, disconnect
from threading import Lock
from state.postmanager import PostManager, PostType

# "threading", "eventlet" or "gevent"
async_mode = 'threading'
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


def serversideEventLoop():
    """Example of how to send server generated events to clients."""
    count = 0
    postmanager = PostManager()
    while True:
        socketio.sleep(1)
        count += 1
        postmanager.add(PostType.POST_TYPE_KAOMOJI)

        socketio.emit('my_response',
                      {'data': postmanager.last().json(), 'count': count},
                      namespace='/eco')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


class EcoTestNamespace(Namespace):
    def on_my_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']})

    def on_disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()

    def on_my_ping(self):
        emit('fps_event')

    def on_connect(self):
        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(
                    target=serversideEventLoop)
        emit('my_response', {'data': 'Connected', 'count': 0})

    def on_disconnect(self):
        print('Client disconnected', request.sid)

socketio.on_namespace(EcoTestNamespace('/eco'))


def launch(host, port, debug):
    socketio.run(app, host=host, port=port, debug=debug)
