Running the main application:

    git submodule init
    git submodule update
    KERAS_BACKEND=tensorflow python run.py --markov_texts_path /mnt/drive1/data/eco/pdf_to_text_postprocessed --keras_models_path /home/marcel/projects/eco/src/python/keras_lstm/models/ --word_lstm_models_path /home/marcel/projects/eco/src/python/word_level_rnn/saved/