let log = $('#log')

class Message {

    constructor(socketMsg) {
        this.text = socketMsg.text
        this.user = socketMsg.user
        this.style = socketMsg.style
        this.attachment = socketMsg.attachment

        this.append()
    }

    append() {
//        log.append('<br>')
        console.log('appending msg')
        log.append($('<div/>').text(this.user +': '+ this.text).attr('class','msg'))
    }
}