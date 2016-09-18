from flask import Flask, render_template, send_file, safe_join, request,jsonify
import imp

grammar = imp.load_source('grammar', '../../tests/grammar.py')

app = Flask(__name__)
app.config.from_object('settings')

@app.route('/', methods=['GET', "POST"])
def index():
    input = request.args.get('grammar')
    if input:
        print input
        if input.startswith('\"'):
            input = input[1:-1]
        output = grammar.correct(input)
        output_json = jsonify(**{"grammar_corrected":output})
        print ">> ",output
        return output_json
    return render_template('index.html')


def launch():
    #global logger

    #logger = get_std_logger("server")
    #logger.debug("Starting Server")
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
    #logger.debug("Application terminates")

# RUN APP
if __name__ == "__main__":
    launch()