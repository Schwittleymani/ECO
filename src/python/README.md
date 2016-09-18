Base code taken from keras/examplse/lstm_text_generation.py

training:

    KERAS_BACKEND=tensorflow python lstm_train.py --input /mnt/drive1/data/eco/txt/marilyn_raffaele-journal2015.txt --iterations 20 --epochs 10 --steps 2 --model_save_path /home/marcel/projects/eco/src/python/models/marilyn_raffaele/marilyn_raffaele_i20e10s2.h5
    
steps: the smaller the better the training, though takes longer
i20e10s2: iterations=20, epochs=10, steps=2

sampling:

    KERAS_BACKEND=tensorflow python lstm_sample.py --model_load_path /home/marcel/projects/eco/src/python/models/marilyn_raffaele/marilyn_raffaele_i20e10s2.h5 --diversity 0.3 --output_length 200