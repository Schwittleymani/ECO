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

### 3. general

##Emojis
Emojis are done with colon Shortcodes e.g. :smile:
good source to get your emojis shortcodes are https://emojipedia.org or https://www.emoji.codes/
It's an outdated emoji version tho... damnit
see the endpart of https://github.com/iamcal/js-emoji/blob/master/lib/emoji.js
to see the actual available list
