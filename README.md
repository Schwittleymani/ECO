# ECO (Electronic Chaos Oracle)

##### Running things on lyrik

    workon eco_tensorflow
    # has python dependencies for all modules installed: 
    # * webserver(src/python/webserver/req.txt)
    # * markov-chain (markovify)
    # * keras-lstm (keras, tensorflow, etc)
    # * word-levelrnn/lstm(tensorflow)
    
    

### Facebook version

Dependencies

    sudo apt-get install nodejs-legacy
    npm install node-osc
    npm install facebook-chat-api

Configuration

- Change this line to contain your facebook plain text login data: https://github.com/mrzl/ECO/blob/master/src/node/facebook-advanced-echo.js#L16
- Adjust the threadId of the person you want to chat with here: https://github.com/mrzl/ECO/blob/master/src/node/facebook-advanced-echo.js#L42 and https://github.com/mrzl/ECO/blob/master/src/node/facebook-advanced-echo.js#L23 (it's being printed when you receive a message. At the moment I haven't fount a better way of getting the threadId of one conversation.)
- Run it via 

    node facebook-eco.js


- Run https://github.com/mrzl/ECO/blob/master/src/main/java/oracle/SimpleOracle.java (or an exported jar.)

#### Client

### for gifs
create the folder in data:
- gifs/clean
- gifs/gify
- gifs/*

gifs are git-ignored and stored on lyrik...

in the config.properties there is a new property called:
DOWNLOAD_GIFY, guess what it does.
You will get the Gif anyway but storing them might be more fun, and it sometimes constructing Gif Object
with an URL seems to fail.

###
Easter eggs
how to use eastereggs
easter eggs are configured in the
data/easteregg.json
Jesus.java loads that file

There are three easteregg Types specified by their possible occurance:
PAUSE: they come up, when the oracle state is userinput but nothing happens for a long time.
INTERRUPT: happen while the user is typing
ANSWER: happen with a bot answer
(possibly also AFTER): after bot answer and user input

e.g. PAUSE: Monolog, ANSWER: emoji, gifs

Each eastergg configuration must contain the the value 'active',
which defines if the egg is used or not.
And 'chance', which sets the chance to occur.
...