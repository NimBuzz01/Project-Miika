import numpy as np
from keras.models import load_model
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input

model = load_model('miika_model.h5')
enc_model = Model([enc_inp], enc_states)

# decoder Model
decoder_state_input_h = Input(shape=(400,))
decoder_state_input_c = Input(shape=(400,))

decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

decoder_outputs, state_h, state_c = dec_lstm(dec_embed,
                                             initial_state=decoder_states_inputs)

decoder_states = [state_h, state_c]

dec_model = Model([dec_inp] + decoder_states_inputs,
                  [decoder_outputs] + decoder_states)

from keras.preprocessing.sequence import pad_sequences

print("##########################################")
print("#              Project Miika             #")
print("##########################################")

prepro1 = ""
while prepro1 != 'q':
    prepro1 = input("You : ")
    ## prepro1 = "Hello"

    prepro1 = formatText(prepro1)
    ## prepro1 = "hello"

    prepro = [prepro1]
    ## prepro1 = ["hello"]

    txt = []
    for x in prepro:
        # x = "hello"
        tempList = []
        for y in x.split():
            ## y = "hello"
            try:
                tempList.append(vocab[y])
                ## vocab['hello'] = 454
            except:
                tempList.append(vocab['<OUT>'])
        txt.append(tempList)

    ## txt = [[454]]
    txt = pad_sequences(txt, 13, padding='post')

    ## txt = [[454,0,0,0,.........13]]

    stat = enc_model.predict(txt)

    empty_target_seq = np.zeros((1, 1))
    ##   empty_target_seq = [0]

    empty_target_seq[0, 0] = vocab['<SOS>']
    ##    empty_target_seq = [255]

    stop_condition = False
    decoded_translation = ''

    while not stop_condition:

        dec_outputs, h, c = dec_model.predict([empty_target_seq] + stat)
        decoder_concat_input = dense(dec_outputs)
        ## decoder_concat_input = [0.1, 0.2, .4, .0, ...............]

        sampled_word_index = np.argmax(decoder_concat_input[0, -1, :])
        ## sampled_word_index = [2]

        sampled_word = inv_vocab[sampled_word_index] + ' '

        ## inv_vocab[2] = 'hi'
        ## sampled_word = 'hi '

        if sampled_word != '<EOS> ':
            decoded_translation += sampled_word

        if sampled_word == '<EOS> ' or len(decoded_translation.split()) > 13:
            stop_condition = True

        empty_target_seq = np.zeros((1, 1))
        empty_target_seq[0, 0] = sampled_word_index
        ## <SOS> - > hi
        ## hi --> <EOS>
        stat = [h, c]

    print("Miika : ", decoded_translation)
    print("==============================================")
