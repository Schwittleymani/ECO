from flask import Flask, render_template, send_file, safe_join, request,jsonify
from threading import Thread
from flask_socketio import SocketIO

import settings


app = Flask(__name__)
app.config.from_object('settings')
socketio = SocketIO(app)



@app.route('/', methods=['GET', "POST"])
def index():
        return render_template('index.html')


@app.route('/input', methods=["POST"])
def input():
    print "input..."
    #print request.json()
    values = request.values
    #print values
    inputS = None
    try:
        inputS = values['inputS']
    except TypeError:
        return jsonify({'status': 'no-input', 'response': get_answer()})
    print inputS

    #text = request.json['inputS']
    return render_template('index.html')



def launch():
    def start_websocket_server():

        socketio.run(app, port=app.config['PORT_WEBSOCKET'])
    #Thread(target=start_websocket_server).start()
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])

    #logger.debug("Application terminates")

# RUN APP
if __name__ == "__main__":
    launch()
