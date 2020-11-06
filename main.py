# Todd McCullough  June 29 2020

from flask import Flask
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

import cb_main as cbu

import numpy as np
import pandas as pd


theme = 'demon'
chatbot = 'Demonicus'
title = 'Speak To '+chatbot

chats = Flask(__name__)

# index root for the chatbot
@chats.route('/index')
def index():
    generated_text = pd.read_csv('datasets/chatbot-users-testing.csv')
    print(generated_text['responses'])

    return render_template('index.html',
    generated_text = generated_text, description = description,
    theme = theme, title = title, chatbot = chatbot)

# generated chats will end up here
@chats.route('/generate', methods=['POST'])
def generate():
    sentence = request.form['generate']
    generated_text = cbu.generate_text(start_string=sentence+u'\n',temperature = 0.9)

    return render_template('index.html',
    generated_text = generated_text, description = description,
    theme = theme, title = title, chatbot = chatbot)

# testing section
@chats.route('/chat')
def chat():
    generated_text = pd.read_csv('datasets/chatbot-users-responses.csv')

    return render_template('chats.html',
    generated_text = generated_text,
    theme = theme, title = title, chatbot = chatbot)

if __name__ == "__main__":
    chats.run()
