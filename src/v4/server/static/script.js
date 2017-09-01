let log = $('#log')
let template = $('#msgTemplate')

let nextMsgRight = false

var emoji = new EmojiConvertor();

appendMsg(socketMsg) {
    var text = socketMsg.text;
    var user = socketMsg.user;
    var attachment = socketMsg.attachment;
    var style = socketMsg.style;
}

class Message {

    constructor(socketMsg) {
        this.text = emoji.replace_colons(socketMsg.text)
        console.log(this.text)
        this.user = socketMsg.user
        this.style = socketMsg.style
        this.attachment = socketMsg.attachment

        this.append()
        nextMsgRight = !nextMsgRight
    }

    append() {
//        log.append('<br>')
        console.log('appending msg')
        let msgObj = template.clone()
        msgObj.removeAttr('id')
        msgObj.find('.msgText').text(this.text)
        msgObj.find('.msgUser').text(this.user)
        //if(nextMsgRight)
            msgObj.find('.msgBox').addClass('rightMsgBox')
        log.append(msgObj)
//        log.append($('<div/>').text(this.user +': '+ this.text).attr('class','msg'))
    }
}