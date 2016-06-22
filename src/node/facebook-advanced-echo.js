var osc = require('node-osc')
var client = new osc.Client('127.0.0.1', 12000);

var server = new osc.Server(12001, '127.0.0.1');
server.on("message", function (msg, rinfo) {
    console.log("new msg");
    console.log(msg);
});

var login = require("facebook-chat-api");

login({email: "email", password: "password", pageID: 1728943587378130}, function callback (err, api) {
    if(err) return console.error(err);

    var server = new osc.Server(12001, '127.0.0.1');
    server.on("message", function (msg, rinfo) {
        console.log(msg);
        api.sendMessage(msg[1], msg[2]);
    });

    api.setOptions({selfListen: false, listenEvents: true, pageID: 1728943587378130});

    var stopListening = api.listen(function(err, event) {
        if(err) return console.error(err);

        switch(event.type) {
            case "message":
                api.markAsRead(event.threadID, function(err) {
                    if(err) console.log(err);
                });
                client.send("/get", event.body, event.threadID);

                console.log("msg: " + event.body);
                console.log("theadid: " + event.threadID)
                break;
            case "event":
                console.log(event);
                break;
        }
    });
});
