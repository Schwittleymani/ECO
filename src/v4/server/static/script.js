let log = $('#log')
let template = $('#msgTemplate')
let nextMsgRight = false

var emoji = new EmojiConvertor();

function appendMsg(socketMsg) {
    var text = emoji.replace_colons(socketMsg.text);
    var user = socketMsg.user;
    var attachment = socketMsg.attachment;
    var style = socketMsg.style;
    var timestamp = socketMsg.timestamp;

    var msgObj = template.clone()
    msgObj.removeAttr('id')

    msgObj.find('.timeStamp').text("<b>" + user + "</b>: " + timestamp)

    // checking whether the text should be added to a
    // <pre> (pre-formatted) or <div> tag
    // important for pre-formatted text like ascii stuff
    // TODO style is supposed to be a more complex object, but for now... ok
    // TODO let's also have a default style use its string representation on the top of the file.
    // this is magic number style and often leads to problems when another developer cannot read your mind
    if(style == "unformatted") {
        msgObj.find('.msgTextDiv').text(text)
    } else if (style == "formatted") {
        msgObj.find('.msgTextPre').text(text)
    }

    // inserts username
    msgObj.find('.msgUser').text(user)

    // adds some css class to divs for left and right style
    msgObj.find('.msgBox').addClass(nextMsgRight ? 'right' : 'left')

    // adds the customized msg to the log
    log.append(msgObj)

    nextMsgRight = !nextMsgRight
}

