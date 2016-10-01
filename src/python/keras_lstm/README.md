Base code taken from keras/examplse/lstm_text_generation.py

training:

    KERAS_BACKEND=tensorflow python lstm_train.py --input /mnt/drive1/data/eco/pdfre_postprocessed/sherry_turkle-the_second_self_computers_and_the_human_spirit.txt --iterations 3 --epochs 10 --steps 2 --model_save_path /home/marcel/projects/eco/src/python/keras_lstm/models/sherry_turkle/sherry_turkle-the_second_self_computers_and_the_human_spirit_i03e10s2.h5 >> logs/sherry_turkle-the_second_self_computers_and_the_human_spirit_i03e10s2.log
    
* steps: the smaller the better the training, though takes longer
* i20e10s2: iterations=20, epochs=10, steps=2

sampling:

    KERAS_BACKEND=tensorflow python lstm_sample.py --model_load_path /home/marcel/projects/eco/src/python/keras_lstm/models/marilyn_raffaele/marilyn_raffaele_i20e10s2.h5 --diversity 0.3 --output_length 200