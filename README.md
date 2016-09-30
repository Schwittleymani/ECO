# ECO (Electronic Chaos Oracle)

##### Running things on lyrik

    workon eco_tensorflow
    # has python dependencies for all modules installed: 
    # * webserver(src/python/webserver/req.txt)
    # * markov-chain (markovify)
    # * keras-lstm (keras, tensorflow, etc)
    # * word-levelrnn/lstm(tensorflow)
    
    

### Facebook version
- Change this line to contain your facebook plain text login data: https://github.com/mrzl/TheOracle/blob/master/src/node/facebook-advanced-echo.js#L16
- Adjust the threadId of the person you want to chat with here: https://github.com/mrzl/TheOracle/blob/master/src/node/facebook-advanced-echo.js#L42 and https://github.com/mrzl/TheOracle/blob/master/src/node/facebook-advanced-echo.js#L23 (it's being printed when you receive a message. At the moment I haven't fount a better way of getting the threadId of one conversation.)
- Run it via 
```
node facebook-advanced-echo.js
```
- Run https://github.com/mrzl/TheOracle/blob/master/src/main/java/oracle/SimpleOracle.java (or an exported jar.)


### for gifs
create the folder in data:
- gifs/clean
- gifs/gify
- gifs/*

gifs are git-ignored and stored on lyrik...

