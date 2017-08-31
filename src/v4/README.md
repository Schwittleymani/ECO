## temp readme howto

### 0. setup

    # setup git-lsf
    cd ~/Downloads/
    wget https://github.com/git-lfs/git-lfs/releases/download/v2.2.1/git-lfs-linux-amd64-2.2.1.tar.gz
    tar xvf git-lfs-linux-amd64-2.2.1.tar.gz
    sudo git-lfs-2.2.1/install.sh

    # git-lfs installed yay

    cd ECO
    # follow this for adding large files:
    # https://git-lfs.github.com/


### 1. start webserver

    workon v4
    cd src/v4
    pip install -r requirements.txt
    python server/webserver.py

### 2. start posting

    workon v4
    cd src/v4
    pip install -r requirements.txt
    python run.py