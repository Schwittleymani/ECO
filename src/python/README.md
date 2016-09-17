Base code taken from keras/examplse/lstm_text_generation.py

training:

    KERAS_BACKEND=tensorflow python lstm_train.py --input /mnt/drive1/data/eco/txt/marilyn_raffaele-journal2015.txt --iterations 30 --epochs 20 --max_input_length 20 --model_save_path /home/marcel/projects/eco/src/python/models
    
sampling:

    KERAS_BACKEND=tensorflow python lstm_sample.py --model_load_path /home/marcel/projects/eco/src/python/models/marilyn_raffaele/ --diversity 0.3 --seed 'yeah' --output_length 200