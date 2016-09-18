from flask import Flask, render_template, send_file, safe_join, request,jsonify
import imp, sys
import time
from threading import Thread

import settings
from StandardAnswers import get_answer
grammar = imp.load_source('grammar', '../../tests/grammar.py')

app = Flask(__name__)
app.config.from_object('settings')

'''
not crazy robust so I'll leave the issue open.
the ml thread is not killed.
you don't just kill threads in python...
... how to behave when another input is sent...

also fails and sents status 400 when sent data does not contain 'inputS'


'''

def grammar_check(input):
    print input
    if input.startswith('\"'):
        input = input[1:-1]
    output = grammar.correct(input)
    output_json = jsonify(**{"grammar_corrected": output})
    print ">> ", output
    return output_json

@app.route('/', methods=['GET', "POST"])
def index():
    # grammar test
    input = request.args.get('grammar')
    if input:
        return grammar_check(input())
    else:
        return render_template('index.html')


@app.route('/input', methods=["POST"])
def input():
    '''
    main function to get a return from machine
    :return:
    '''
    values = request.values
    #print values
    inputS = None
    try:
        inputS = values['inputS']
    except TypeError:
        return jsonify({'status': 'no-input', 'response': get_answer()})
    print inputS
    response = {}
    def ml_magic(inputS):

        try:
            print "CALL ML MAGIC HERE... for: ",inputS
            ## when its cool
            response['status'] = 'ml-response'
            response['response'] = "ML RESPONSE"
        except:
            print("Unexpected error:", sys.exc_info()[0])
            response['status'] = 'error'

    ml_thread = Thread(target=ml_magic, args=(inputS,))
    ml_thread.start()
    ml_thread.join(settings.MAX_MACHINE_TIME)
    if ml_thread.is_alive:
        return jsonify(response)
    else:
        return jsonify({'status': 'ml-timeout', 'response': get_answer()})


def launch():
    #global logger

    #logger = get_std_logger("server")
    #logger.debug("Starting Server")
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
    #logger.debug("Application terminates")

# RUN APP
if __name__ == "__main__":
    launch()