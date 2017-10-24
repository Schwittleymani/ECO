var log_div, template, nextMsgRight, emoji;

window.onload = function () {
    log_div = $('#log');
    template = $('#msgTemplate');
    nextMsgRight = false;
    emoji = new EmojiConvertor();
};

function text2emoji(t){
    var text = emoji.replace_colons(t);
    text = emojione.toImage(text);
    text = EmojiTranslate.translate(text);
    return text;
}

document.addEventListener('keydown', function(event) {
    // a-zA-Z and space
    if((event.which > 64 && event.which < 91) || event.which === 32) {
        var t = log_div.find('li:last').find('.timeStamp');
        console.log(t);
        if (t.text().indexOf('interactive') !== -1) {
            var d = log_div.find('li:last').find('.msgTextDiv');

            d.append(event.key);
        }
        //event.preventDefault();
    }

    // enter
    if(event.which === 8)
    {
        var d = log_div.find('li:last').find('.msgTextDiv').text();
    }
}, false);

function appendMsg(socketMsg) {
    var text = socketMsg.text;
    var user = socketMsg.user;
    var attachment = socketMsg.attachment;
    var style = socketMsg.style;
    var timestamp = socketMsg.timestamp;

    var msgObj = template.clone();

    var styles = style.split(";");
    for (var i = 0; i < styles.length; i++) {
        if(styles[i] === "emojify")
        {
            text = text2emoji(text);
        }
        if(styles[i] === "unfortmatted")
        {
            msgObj.find('.msgTextDiv').html(text);
        }
        if(styles[i] === "formatted")
        {
            msgObj.find('.msgTextPre').html(text);
        }
        if(styles[i] === "scroll")
        {
            msgObj.find('.canScroll').addClass("scrollDiv");
            msgObj.find('.msgTextDiv').html(text);
            msgObj.find('.msgTextDiv').addClass(nextMsgRight ? 'right' : 'left');
        }
        if(styles[i] === "spritz")
        {
            var spritz = new Spritzer(msgObj.find('.canScroll').get(0));
            spritz.render(text, 230);
        }
    }

    // when there are more than 100 posts
    // remove the first 70
    // it's like that because otherwise the
    // scrolling is getting fucked up
    if( log_div.children().length > 100) {
        var counter = 0;
        log_div.children().each(function() {
            counter = counter + 1;
            if( counter < 70 ){
                $( this ).remove();
            }
        });
        //log_div.find('li:first').remove()
    }

    msgObj.find('.timeStamp').html(emojione.toImage(user) + ": " + timestamp);


    if( attachment === null) {
        // remove the image tag
        msgObj.find('.image').remove();
    } else {
        // append the image and remove the text
        msgObj.find('.image').attr( 'src', attachment );
        msgObj.find('.msgTextDiv').remove();
        msgObj.find('.msgTextPre').remove();
    }

    // adds some css class to divs for left and right style
    msgObj.find('.msgBox').addClass(nextMsgRight ? 'right' : 'left');
    msgObj.find('.timeStamp').addClass(nextMsgRight ? 'right' : 'left');

    msgObj.effect( "pulsate", {times:5}, 3000 );

    // adds the customized msg to the log
    log_div.append(msgObj);

    nextMsgRight = !nextMsgRight;
}

