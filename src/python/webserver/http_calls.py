from threading import Thread
from flask import request,jsonify
import imp

import webserver.settings
from postpreprocess.spell_check import PreProcessor

preProc = PreProcessor()

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