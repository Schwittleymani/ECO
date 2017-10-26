
import model
import server

"""
phone : wifi hotspot
Pi > printer ))) phone
laptop model/server ))) phone
laptop ssh > pi

laptop and pi connedt to the phone (hotspot)
laptop logins to the pi over ssh
laptop creates a server.
laptop calls a script on the pi that makes a request to the server(laptop)
to ask for a fortune
"""


if __name__ == "__main__":
    model.load_model()
    server.launch()
