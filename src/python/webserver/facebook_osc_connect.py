import OSC
import threading
import unicodedata

class OscFacebook(object):
    def __init__(self):
        receive_address = ('localhost', 12000)
        send_address = 'localhost', 12001

        print("Facebook service started")

        self.server = OSC.OSCServer(receive_address)
        self.client = OSC.OSCClient()
        self.client.connect(send_address)
        self.client.print_tracebacks = True

        self.server_thread = threading.Thread(target=self.server.serve_forever)
        # daemon means, when main app quits, the thread is done too
        self.server_thread.daemon = True
        self.server_thread.start()

    def send(self, text, threadid):
        print('trying to send ' + text + ' to ' + threadid)
        print(type(text))
        if isinstance(text, unicode):
            print('input was unicode, so encodign in ascii')
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
        msg = OSC.OSCMessage('/answer')
        msg.append(text)
        msg.append(int(threadid))
        self.client.send(msg)

    def add_callback(self, pattern, func):
        print('adding callback')
        self.server.addMsgHandler(pattern, func)

if __name__ == '__main__':

    def received(addr, tags, stuff, source):
        print(addr)
        print(OSC.getUrlStr(source))

    osc = OscFacebook()
    osc.add_callback('/get', received)

    while True:
        pass