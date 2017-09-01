let log = $('#log')
let template = $('#msgTemplate')

let nextMsgRight = false


class Message {

    constructor(socketMsg) {
        this.text = socketMsg.text
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

        if(this.style == "unformatted") {
            console.log(this.style)
            msgObj.find('.msgTextDiv').text(this.text)
        } else if (this.style == "formatted") {
            console.log(this.style)
            msgObj.find('.msgTextPre').text(this.text)
        }
        msgObj.find('.msgUser').text(this.user)
        //if(nextMsgRight)
            msgObj.find('.msgBox').addClass('rightMsgBox')
        log.append(msgObj)
//        log.append($('<div/>').text(this.user +': '+ this.text).attr('class','msg'))
    }
}