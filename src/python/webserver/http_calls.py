from threading import Thread
from flask import request,jsonify
import imp
import facebook_osc_connect
import generator   
import webserver.settings
from postpreprocess.spell_check import PreProcessor
import settings

import sys
import traceback

queue = []
threadids = []

def process_from_facebook(addr, tags, stuff, source):
    print('FACEBOOK receiving: ', addr, tags, stuff)
    raw_input = stuff[0]
    thread_id = stuff[1]
    processed_input, _, __ = preProc.process(raw_input)
    answer = generator.get_result(processed_input)
    processed_output, _, __ = preProc.process(answer, return_to_lower=True)
    print('FACEBOOK done: ' + processed_output)
    facebook.send(processed_output, thread_id)

preProc = PreProcessor()
generator = None
facebook = facebook_osc_connect.OscFacebook()
facebook.add_callback('/get', process_from_facebook)


def set_generator(gen):
    global generator
    print 'setting gen', gen
    generator = gen


def input(input):
    global generator
    '''
    main function to get a return from machine
    :return:
    '''
    processed_input, _, __ = preProc.process(input)

    response = {}
    def ml_magic(input):

        processed_input, _, __ = preProc.process(input)
        answer = generator.get_result(processed_input)
        processed_output, _, __ = preProc.process(answer, return_to_lower=True)

        try:
            print "CALL ML MAGIC HERE... for: ",processed_output
            response['status'] = 'ml-response'
            response['response'] = processed_output
        except:
            print("Unexpected error:", sys.exc_info()[0])
            traceback.print_exc()
            response['status'] = 'error'

    ml_thread = Thread(target=ml_magic, args=(processed_input,))
    ml_thread.start()
    ml_thread.join(settings.MAX_MACHINE_TIME)
    if ml_thread.is_alive:
        return jsonify(response)
    else:
        return jsonify({'status': 'ml-timeout', 'response': 'boomchickawaowao'})


def text_preproccess(input):
    print input
    if input.startswith('\"'):
        input = input[1:-1]
    # process
    processed,  spell_checked, grammar_checked = preProc.process(input)

    output_json = jsonify(**{"grammar_corrected" : grammar_checked, 
        "spell_checked" : spell_checked, 
        "combined" : processed})
    print ">> ", output_json
    return output_json
