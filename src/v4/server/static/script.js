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
    var text = text2emoji(socketMsg.text);
    var user = socketMsg.user;
    var attachment = socketMsg.attachment;
    var style = socketMsg.style;
    var timestamp = socketMsg.timestamp;

    var msgObj = template.clone();

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

    // checking whether the text should be added to a
    // <pre> (pre-formatted) or <div> tag
    // important for pre-formatted text like ascii stuff
    // TODO style is supposed to be a more complex object, but for now... ok
    // TODO let's also have a default style use its string representation on the top of the file.
    // this is magic number style and often leads to problems when another developer cannot read your mind

    if(style === "unformatted") {
        msgObj.find('.msgTextDiv').html(text);
    } else if (style === "formatted") {
        msgObj.find('.msgTextPre').html(text);
    } else if( style === "scroll") {
        msgObj.find('.canScroll').addClass("scrollDiv");
        msgObj.find('.msgTextDiv').html(text);
        msgObj.find('.msgTextDiv').addClass(nextMsgRight ? 'right' : 'left');
    } else if( style === "spritz") {
        var spritz = new Spritzer(msgObj.find('.canScroll').get(0));
        spritz.render(text, 230);
    }

    console.log(msgObj.find('.msgTextDiv'));

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

    msgObj.effect( "pulsate" );

    // adds the customized msg to the log
    log_div.append(msgObj);

    nextMsgRight = !nextMsgRight;
}

