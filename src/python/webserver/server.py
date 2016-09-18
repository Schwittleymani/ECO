from flask import Flask, render_template, send_file, safe_join, request
import grammar as grammar_check

app = Flask(__name__)
app.config.from_object('settings')

@app.route('/', methods=['GET', "POST"])
def index():
    grammar = request.args.get('grammar')
    if grammar:
        print grammar
        if grammar.startswith(""):
            grammar = grammar[1:-1]
        grammar = grammar_check.correct(grammar)
        print ">> ",grammar
        return "{grammar_correct:"+grammar+"}"
    return render_template('index.html')


def launch():
    #global logger

    #logger = get_std_logger("server")
    #logger.debug("Starting Server")
    app.run(debug=True, host=app.config['HOST'], port=app.config['PORT'])
    #logger.debug("Application terminates")

# RUN APP
if __name__ == "__main__":
    launch()