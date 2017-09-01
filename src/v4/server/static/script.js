let log = $('#log')
let template = $('#msgTemplate')
let nextMsgRight = false

var emoji = new EmojiConvertor();

function appendMsg(socketMsg) {
    var text = emoji.replace_colons(socketMsg.text);
    console.log(text)
    var user = socketMsg.user;
    var attachment = socketMsg.attachment;
    var style = socketMsg.style;

    console.log(style)

    var msgObj = template.clone()
    msgObj.removeAttr('id')

    // checking whether the text should be added to a
    // <pre> (pre-formatted) or <div> tag
    // important for pre-formatted text like ascii stuff
    if(style == "unformatted") {
        console.log(style)
        msgObj.find('.msgTextDiv').text(text)
    } else if (style == "formatted") {
        console.log(style)
        msgObj.find('.msgTextPre').text(text)
    }

    // inserts username
    msgObj.find('.msgUser').text(user)

    // adds some css class to divs for left and right style
    if(nextMsgRight) {
        msgObj.find('.msgBox').addClass('right')
    } else {
        msgObj.find('.msgBox').addClass('left')
    }

    // adds the customized msg to the log
    log.append(msgObj)

    nextMsgRight = !nextMsgRight
}

