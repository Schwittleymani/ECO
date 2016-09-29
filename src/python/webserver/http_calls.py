from threading import Thread
from flask import request,jsonify
import imp

import settings
grammar = imp.load_source('grammar', '../../tests/grammar.py')
from Spellchek import spell_check

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
    # grammar
    grammar_correct_out = grammar.correct(input)
    spell_check_out = spell_check(input)
    output_json = jsonify(**{"grammar_corrected" : grammar_correct_out, "spell_check" : spell_check_out})
    print ">> ", output_json
    return output_json