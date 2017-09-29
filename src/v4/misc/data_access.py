import socket
import subprocess

# GET THE RIGHT FOLDER
# THERE 3 FOLDERS U MIGHT WANNA GET:
# 1. ECO main Project folder, which is a git repo
# 2. The data folder, which has all the corpii
# 3. Model folder, which contains trained models

# FILL THE DICT UP AND USE THE MODULE EVERYWHERE AND ALL THE TIME FOR DATA/MODEL/(ANY FILE) ACCESS

# CALL get_project_folder(), get_data_folder(), get_model_folder() from outside. works on all machines.
# NO MORE HARD CODED FOLDER CHANGES!!!
"""
 .-----------------. .----------------.   .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. | | .--------------. || .--------------. || .--------------. || .--------------. |
| | ____  _____  | || |     ____     | | | | ____    ____ | || |     ____     | || |  _______     | || |  _________   | |
| ||_   \|_   _| | || |   .'    `.   | | | ||_   \  /   _|| || |   .'    `.   | || | |_   __ \    | || | |_   ___  |  | |
| |  |   \ | |   | || |  /  .--.  \  | | | |  |   \/   |  | || |  /  .--.  \  | || |   | |__) |   | || |   | |_  \_|  | |
| |  | |\ \| |   | || |  | |    | |  | | | |  | |\  /| |  | || |  | |    | |  | || |   |  __ /    | || |   |  _|  _   | |
| | _| |_\   |_  | || |  \  `--'  /  | | | | _| |_\/_| |_ | || |  \  `--'  /  | || |  _| |  \ \_  | || |  _| |___/ |  | |
| ||_____|\____| | || |   `.____.'   | | | ||_____||_____|| || |   `.____.'   | || | |____| |___| | || | |_________|  | |
| |              | || |              | | | |              | || |              | || |              | || |              | |
| '--------------' || '--------------' | | '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'   '----------------'  '----------------'  '----------------'  '----------------' 
"""


folders = {
    "lyrik": {
        "ramin": {
            "project": "/home/ramin/projects/ECO/",
            "data": "/mnt/drive1/data/eco/",
            "model": "/mnt/drive1/data/eco/models/" #"LETS HAVE A MODELS FOLDER ON /mnt/drive1"
        },
        "marcel": {
            "project": "/home/marcel/projects/eco/",
            "data": "/mnt/drive1/data/eco/",
            "model": "/mnt/drive1/data/eco/models/"
        },
    },
    "ramin.local": {
        "raminsoleymani": {
            "project": "/Users/raminsoleymani/git/ECO/",
            "data": "/Users/raminsoleymani/git/ECO/data/", # locally we might have data & models here ( & in .gitignore)
            "model": "/Users/raminsoleymani/git/ECO/models/"
        }
    },
    "mrzl.FILLIN": {
        "mrzlo":{
            "project": "",
            "data": "",
            "model": ""            
        }
    },
}


def _get_hostname():
    return socket.gethostname()

def _get_user():
    result = subprocess.run(['id', '-un'], stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip()

def _machine_folder(specific = 'project'):
    return folders[_get_hostname()][_get_user()][specific]

def get_project_folder():
    return _machine_folder()
    
def get_data_folder():
    return _machine_folder('data')


def get_model_folder():
    return _machine_folder('model')

# TESTIN
if __name__ == "__main__":
    print("get_project_folder():", get_project_folder())
    print("get_data_folder():", get_data_folder())
    print("get_model_folder():", get_model_folder())