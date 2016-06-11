var osc = require('node-osc')
var client = new osc.Client('127.0.0.1', 12000);

var server = new osc.Server(12001, '127.0.0.1');
server.on("message", function (msg, rinfo) {
    console.log("new msg");
    console.log(msg);
});

var login = require("facebook-chat-api");
// Simple echo bot. He'll repeat anything that you say.
// Will stop when you say '/stop'



login({email: "EMAIL", password: "PASSWORD"}, function callback (err, api) {
    if(err) return console.error(err);

    var server = new osc.Server(12001, '127.0.0.1');
    server.on("message", function (msg, rinfo) {
        console.log("new msg");
        console.log(msg);
        api.sendMessage(msg[1], 649026641);
    });


    api.setOptions({listenEvents: true});

    var stopListening = api.listen(function(err, event) {
        if(err) return console.error(err);

        switch(event.type) {
          case "message":
            if(event.body === '/stop') {
              api.sendMessage("Goodbye...", event.threadID);
              return stopListening();
            }
            //api.markAsRead(event.threadID, function(err) {
            //  if(err) console.log(err);
            //});
            try {
              if(event.threadID == 649026641 ) {
                  //client.send("/get", event.body);
                  api.markAsRead(event.threadID, function(err) {
                      if(err) console.log(err);
                  });
                client.send("/get", event.body);
              }
              console.log("msg: " + event.body);
              console.log("theadid: " + event.threadID)
            } catch(e) {
              console.log("couldnt do anything with his")
            }
            break;
          case "event":
            console.log(event);
            break;
        }
    });
});
