## 0. setup

    # setup git-lsf
    cd ~/Downloads/
    wget https://github.com/git-lfs/git-lfs/releases/download/v2.2.1/git-lfs-linux-amd64-2.2.1.tar.gz
    tar xvf git-lfs-linux-amd64-2.2.1.tar.gz
    sudo git-lfs-2.2.1/install.sh

    # git-lfs installed yay

    cd ECO
    # follow this for adding large files:
    # https://git-lfs.github.com/


## 1. start webserver

    workon v4
    cd src/v4
    pip install -r requirements.txt
    python server/webserver.py

## 2. start posting

    workon v4
    cd src/v4
    pip install -r requirements.txt
    python run.py
    // python run.py --replay logs/2017-10-31_16:53:55.700672.json (to replay a older version)


### Training Techniques

#### images

##### 0. porn/non-porn images

    workon v4
    cd src/v4/misc/porn_detector
    # edit porn_detector.py for image path and output json file
    python porn_detector.py

##### 1. classified image databases

    workon v4
    cd src/v4/mist/darknet
    # edit darknet_classify.py to either use classify_non_porn() or classify_4chan_folders()
    # classify_non_porn() uses a file with each line the path to an image (using the output of step 0.)
    # classify_4chan_folders() uses a path to a folder and scans all images
    python darknet_classify.py

##### 2. search this json file

    workon v4
    cd src/v4/posts/image
    python image.py

#### w2v feather similarity

    workon v4
    cd src/v4/notebooks
    jupyter notebook
    # run pandas_w2v_dataframes.ipynb

#### markov chains w/ backoff

    workon v4
    cd src/v4/posts/markov
    python markov.py
    # markov = MarkovManager()
    # markov.train()

#### rvae

    workon v4
    # git submodule init
    # git submodule update
    cd src/v4/pytorch_RVAE
    # create files pytorch_RVAE/Featherstone_Mike_SPLIT/train.txt & pytorch_RVAE/Featherstone_Mike_SPLIT/text.txt
    python train.py --author Featherstone_Mike_SPLIT && python sample.py --author Featherstone_Mike_SPLIT
    # the result should be pytorch_RVAE/Featherstone_Mike_SPLIT-100000samples.txt

#### d2v similarity

    workon v4
    cd src/python/notebooks
    jupyter notebook
    # check Doc2VecSimilarities.ipynb