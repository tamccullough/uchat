# Todd McCullough  June 29 2020

from flask import Flask
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

import calendar
import cb_main as cbu

import numpy as np
import pandas as pd

from datetime import date, datetime, timedelta

theme = 'demon'
chatbot = 'Ouija'
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
year = datetime.today().strftime('%Y')

chats = Flask(__name__)

# index root for the chatbot
@chats.route('/')
def index():
    chats = pd.read_csv('datasets/chat_history.csv')
    chats = chats.tail(6)
    chats = chats.reset_index()
    chats.pop('index')
    chats['month'] = chats['month'].apply(lambda x: calendar.month_name[x])
    print(chats)
    print(post_time, today_other,month, day, weekday)

    return render_template('index.html',
    generated_text = chats, today = today_other, post_time = post_time, period = period,
    month = month, day = day,
    theme = theme, title = title, chatbot = chatbot)

# post user's text before getting the prediction or other function result
@chats.route('/~', methods=['GET','POST'])
def post():
    chats = pd.read_csv('datasets/chat_history.csv')

    num = chats['num'].tail(1).values[0]
    month_num = datetime.today().strftime('%m')
    sentence = request.form['generate']
    new_chat = pd.DataFrame([[num+1, month_num, day, year, weekday, 'you',sentence]],columns=chats.columns)
    chats = pd.concat([chats,new_chat])

    chats.to_csv('datasets/chat_history.csv',index=False)
    chats = pd.read_csv('datasets/chat_history.csv')
    chats = chats.tail(6)
    chats = chats.reset_index()
    chats.pop('index')
    chats['month'] = chats['month'].apply(lambda x: calendar.month_name[int(x)])

    return render_template('chats.html',
    generated_text = chats, today = today_other, post_time = post_time, period = period,
    month = month, day = day,
    theme = theme, title = title, chatbot = chatbot)

# generated chats will end up here
@chats.route('/-')
def generate():
    chats = pd.read_csv('datasets/chat_history.csv')

    month_num = datetime.today().strftime('%m')
    sentence = chats['text'].tail(1).values[0]
    generated_chat = cbu.generate_text(start_string=sentence+u'\n',temperature=0.45)
    num = chats['num'].tail(1).values[0]
    nomed_chat = pd.DataFrame([[num+1, month_num, day, year, weekday, 'nomed',generated_chat]],columns=chats.columns)
    chats = pd.concat([chats,nomed_chat])
    print('dataframe 2\n',chats,'\n')
    print('\nNOW',post_time, today_other,month, day, weekday)

    chats.to_csv('datasets/chat_history.csv',index=False)
    chats = pd.read_csv('datasets/chat_history.csv')
    chats = chats.tail(6)
    chats = chats.reset_index()
    chats.pop('index')
    chats['month'] = chats['month'].apply(lambda x: calendar.month_name[int(x)])


    return render_template('index.html',
    generated_text = chats, today = today_other, post_time = post_time, period = period,
    month = month, day = day,
    theme = theme, title = title, chatbot = chatbot)

if __name__ == "__main__":
    chats.run()
