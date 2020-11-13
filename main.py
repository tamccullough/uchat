# Todd McCullough  June 29 2020

from flask import Flask
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

import cb_main as cbu

import numpy as np
import pandas as pd

from datetime import date, datetime, timedelta

theme = 'demon'
chatbot = 'Nomedicus'
title = 'Talk To '+chatbot

today_other = date.today()
current_time = datetime.now().time()
hour = int(str(current_time)[0:2])
minute = str(current_time)[3:5]
period = 'AM'
if hour > 12:
    hour -= 12
    period = 'PM'
post_time = str(hour)+':'+minute
month, day, weekday = cbu.get_weekday()

chats = Flask(__name__)

# index root for the chatbot
@chats.route('/')
def index():
    chats = pd.read_csv('datasets/chat_history.csv')
    chats = chats.tail(6)
    print(chats)
    print(post_time, today_other,month, day, weekday)

    return render_template('index.html',
    generated_text = chats, today = today_other, post_time = post_time, period = period,
    month = month, day = day,
    theme = theme, title = title, chatbot = chatbot)

# generated chats will end up here
@chats.route('/speak', methods=['GET','POST'])
def speak():
    sentence = request.form['generate']
    chats = pd.read_csv('datasets/chat_history.csv')
    generated_chat = cbu.generate_text(start_string=sentence+u'\n', temperature=0.45)

    return render_template('index.html',
    generated_text = chats,
    theme = theme, title = title, chatbot = chatbot)

# testing section
@chats.route('/chat')
def chat():
    chats = pd.read_csv('datasets/chat_history.csv')

    return render_template('chats.html',
    generated_text = chats,
    theme = theme, title = title, chatbot = chatbot)

@chats.route('/testing', methods=('GET', 'POST'))
def testing():
    return render_template('testing.html',
    theme = theme, title = title, chatbot = chatbot)

if __name__ == "__main__":
    chats.run()
