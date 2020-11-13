# Chat-U
# Todd McCullough 2020
#import tensorflow as tf
#from tensorflow import keras
import numpy as np
import pandas as pd
import os
import time
import tensorflow as tf

from datetime import date, datetime, timedelta

chats_predict = tf.keras.models.load_model('model/chats_saved.h5', compile=False)

path_to_file = 'datasets/chats.txt'# Read, then decode for py2 compat.
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
vocab = sorted(set(text))

vocab_size = len(vocab) # Length of the vocabulary in chars
embedding_dim = 256 # The embedding dimension
rnn_units = 1024 # Number of RNN units

# Creating a mapping from unique characters to indices
char2idx = {u:i for i, u in enumerate(vocab)}
idx2char = np.array(vocab)

text_as_int = np.array([char2idx[c] for c in text])

def generate_text(start_string,temperature):
    # Evaluation step (generating text using the learned model)

    # Number of characters to generate
    num_generate = 250

    # Converting our start string to numbers (vectorizing)
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store our results
    text_generated = []

    # Low temperatures results in more predictable text.
    # Higher temperatures results in more surprising text.
    # Experiment to find the best setting.

    # Here batch size == 1
    chats_predict.reset_states()
    for i in range(num_generate):
        predictions = chats_predict(input_eval)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)

        # using a categorical distribution to predict the character returned by the model
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

        # We pass the predicted character as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx2char[predicted_id])
    responses = ''.join(text_generated)

    if responses.splitlines()[0] == '':
        return responses.splitlines()[1]
    else:
        return responses.splitlines()[0]

# get the weather
from pyowm import OWM

def get_weather(location):
    owm = OWM('a14eef3d1a1226ef3927f87f1fb47f22')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(location)
    w = observation.weather
    # Weather details
    #w.wind()                  # {'speed': 4.6, 'deg': 330}
    #w.humidity                # 87
    #w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    temperature_dict = w.temperature('celsius')
    temperature = temperature_dict.get('temp')
    return temperature
    # https://github.com/csparpa/pyowm

def get_weekday():
    weekDays = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
    current_year = date.today().strftime('%Y')
    month = datetime.today().strftime('%B')
    today = datetime.today()
    day = datetime.today().strftime('%d')

    weekday_num = today.weekday()
    weekday = weekDays[weekday_num]
    return month, day, weekday
