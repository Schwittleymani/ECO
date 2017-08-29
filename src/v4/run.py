from server import webserver
from server import settings

if __name__ == "__main__":
    webserver.launch(settings.HOST, settings.PORT, settings.DEBUG)