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
        let msgObj = template.clone()
        msgObj.removeAttr('id')

        // checking whether the text should be added to a
        // <pre> (pre-formatted) or <div> tag
        // important for pre-formatted text like ascii stuff
        if(this.style == "unformatted") {
            console.log(this.style)
            msgObj.find('.msgTextDiv').text(this.text)
        } else if (this.style == "formatted") {
            console.log(this.style)
            msgObj.find('.msgTextPre').text(this.text)
        }

        // inserts username
        msgObj.find('.msgUser').text(this.user)

        // adds some css class to divs for left and right style
        if(nextMsgRight) {
            msgObj.find('.msgBox').addClass('right')
        } else {
            msgObj.find('.msgBox').addClass('left')
        }

        // adds the customized msg to the log
        log.append(msgObj)
    }
}