from flask import Flask, render_template, request
import json
import serial
import codecs
import model

#,template_folder='src/fortune/templates'
app = Flask(__name__)
printer = None

def write(serial_,s):
    if not serial_:
        return False
    try:
        serial_.write(bytes(s,'utf-8'))
        return True
    except serial.serialutil.SerialException:
        return False


def setup_serial():
    global printer
    try:
        printer = serial.Serial('/dev/cu.usbserial-A703BXBS',19200)
        # center
        write(printer, chr(27))
        write(printer, chr(97))
        write(printer, chr(1))
        # bold
        write(printer, chr(27))
        write(printer, chr(69))
        write(printer, chr(True))
        # speed or something
        write(printer, chr(27))
        write(printer, chr(55))
        write(printer, chr(255))
        write(printer, ("\n"*3))
        print("printer cool")
    except serial.serialutil.SerialException:
        print("printer problems")

HOST = '0.0.0.0'
PORT = 9000
DEBUG = False

newlines = 2

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def print_it_out_motherfucka(sentence):

        # center
        success = write(printer, chr(27))
        if not(success):
            return False
        write(printer, chr(97))
        write(printer, chr(1))
        # normal size
        write(printer, chr(27))
        write(printer, chr(33))
        write(printer, chr(False))

        write(printer,sentence + ('\n' * newlines))
        # small font
        write(printer, chr(27))
        write(printer, chr(33))
        write(printer, chr(True))
        # right justify
        write(printer, chr(27))
        write(printer, chr(97))
        write(printer, chr(2))

        write(printer,"~ORACLE" + ('\n' * 7))
        return True


def split_right(sentence):
    if len(sentence) <= 32:
        return sentence
    else:
        words = sentence.split(' ')
        sen = ''
        c = 0
        first_in_line = True
        next_break = 30
        for w in words:
            c += (len(w))
            if not first_in_line:
                c += 1
            if c > next_break or len(w) > 32:
                sen += '\n'+w
                c = len(w) + 1
            else:
                if not first_in_line:
                    sen += ' '
                else:
                    first_in_line = False
                sen += w
        print('split to',sen)
        return sen

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
    else:
        result = [model.model.select_random().strip()]
    print(result)
    sentence = split_right(result[0])
    logit(text, mode, result)
    print([(s, len(s)) for s in sentence.split('\n')])
    print_job = print_it_out_motherfucka(sentence)
    send_out = {'fortune': result,"show": False}
    if not print_job:
        print("Printer problems")
        setup_serial()
        send_out['show'] = True
    answer = json.dumps(send_out), 200, {'ContentType': 'application/json'}
    return answer #render_template('index.html')


def logit(text, mode, result):
    with codecs.open('log.txt','a',encoding='utf-8') as fout:
        fout.write(json.dumps({'input':text,'mode':mode,'result':result})+'\n')

def launch():
    setup_serial()
    app.run(host=HOST, port=PORT, debug=True)
