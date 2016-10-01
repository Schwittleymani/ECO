Running the main application:

    git submodule init
    git submodule update
    KERAS_BACKEND=tensorflow python run.py --markov_texts_path /mnt/drive1/data/eco/pdf_to_text_postprocessed --keras_models_path /home/marcel/projects/eco/src/python/keras_lstm/models/ --word_lstm_models_path /home/marcel/projects/eco/src/python/word_level_rnn/saved/
    
    The interactive mode can be switched on/off with --interactive. Per default it's set to the value defined in settings.py (INTERACTIVE)
    The interactive mode can be exited, by typing 'exit' as input. 
    
    The webserver starts when START_WEBSERVER in settings.py is set. The Server comes before the interactive mode. It does not run in     parallel or something weird. The server runs on port 8090. It has various settings in webserver/settings.py
