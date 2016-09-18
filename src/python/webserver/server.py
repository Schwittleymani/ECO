from flask import Flask, render_template, send_file, safe_join, request
import imp

grammar = imp.load_source('grammar', '../../tests/grammar.py')

app = Flask(__name__)
app.config.from_object('settings')

@app.route('/', methods=['GET', "POST"])
def index():
    input = request.args.get('grammar')
    if input:
        print input
        if input.startswith(""):
            input = input[1:-1]
            input = grammar.correct(input)
        print ">> ",grammar
        return "{grammar_corrected:"+input+"}"
    return render_template('index.html')


def launch():
    #global logger

    #logger = get_std_logger("server")
    #logger.debug("Starting Server")
    app.run(debug=False, host=app.config['HOST'], port=app.config['PORT'])
    #logger.debug("Application terminates")

# RUN APP
if __name__ == "__main__":
    launch()