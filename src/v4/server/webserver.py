from flask import Flask, render_template, send_file, safe_join, request,jsonify
from flask_socketio import SocketIO, emit
from src.v4.server import settings

app = Flask(__name__)
app.config.from_object('src.v4.server.settings')
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# @socketio.on('key')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))
#
@socketio.on('connect')
def client_connect():
    # emit('my_response', {'data': 'Connected', 'count': 0}, broadcast=True)
    send_msg('hello','mozart')

def send_msg(text, user, style='', attachment=''):
    emit('msg',{
        'text' : text,
        'user': user,
        'style': style,
        'attachment': attachment
    }, broadcast=True)

def launch():
    print('starting webserver')
    socketio.run(app,host= settings.HOST, port=settings.PORT)

# RUN APP
if __name__ == "__main__":
    launch()
