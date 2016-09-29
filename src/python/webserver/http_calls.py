from threading import Thread
from flask import request,jsonify
import imp

import generator   
import webserver.settings
from postpreprocess.spell_check import PreProcessor
import settings

import sys
import traceback

preProc = PreProcessor()
generator = None

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

        try:
            print "CALL ML MAGIC HERE... for: ",input
            response['status'] = 'ml-response'
            response['response'] = generator.print_result(input)
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
        return jsonify({'status': 'ml-timeout', 'response': get_answer()})


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
