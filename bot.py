# -*- coding: utf-8 -*-
import redis
import os
import telebot
import math
import random
import threading
import info
import test
from telebot import types
from emoji import emojize
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

games={}


@bot.message_handler(commands=['start'])
def start(m):
    x=m.text.split('/start')
    if len(x)==2:
       try:
        if m.from_user.id not in games[int(x[1])]['players']:
          if int(x[1])<0:
            i=0
            for ids in games[int(x[1])]['players']:
                i+=1
            games[int(x[1])]['players'].update(createuser(m.from_user.id, m.from_user.first_name, i+1))
            bot.send_message(m.from_user.id, 'Вы успешно присоединились!')
       except:
        if m.chat.id==m.from_user.id:
            bot.send_message(m.from_user.id, 'Игра crossfire')

@bot.message_handler(commands=['startgame'])
def startgame(m):
    if m.chat.id not in games:
        t=threading.Timer(20, begin, args=[m.chat.id])
        t.start()
        games.update(creategame(m.chat.id))
        Keyboard=types.InlineKeyboardMarkup()
        Keyboard.add(types.InlineKeyboardButton(text='Join', url='telegram.me/crossfirebot?start='+str(m.chat.id)))
        bot.send_message(m.chat.id, 'Присоединиться', reply_markup=Keyboard)
    else:
        bot.send_message(m.chat.id, 'Игра уже запущена! Жмите "присоединиться"!')
    
   
def begin(id):
    if len(games[id]['players'])>1:
        bot.send_message(id, 'Игра начинается!')
        xod(games[id])
    else:
        bot.send_message(id, 'Недостаточно игроков!')
        del games[id]


def xod(game):
    if len(game['players'])==2:
        roles=['agent','killer']
    elif len(game['players'])==5:
        roles=['agent','killer', 'glavar', 'prohojii', 'primanka']
    pick=[]
    for g in game['players']:
        x=random.randint(0, len(game['players'])-1)
        while x in pick:
            x=random.randint(0, len(game['players'])-1)
        game['players'][g]['role']=roles[x]
        pick.append(x)
        print(game)
    for g in game['players']:
        if game['players'][g]['role']=='agent':
            text='Ты агент'
        elif game['players'][g]['role']=='killer':
            text='Ты киллер'
        elif game['players'][g]['role']=='prohojii':
            text='Ты прохожий'
        elif game['players'][g]['role']=='primanka':
            text='Ты приманка'
        elif game['players'][g]['role']=='glavar':
            text='Ты главарь'
        bot.send_message(game['players'][g]['id'], text)
    t=threading.Timer(20, shoot, args=[game])
    t.start()
            
        

def shoot(game):
    for g in game['players']:
        Keyboard=types.InlineKeyboardMarkup()
        for ids in game['players']:
            if game['players'][ids]['id']!=game['players'][g]['id']:
                Keyboard.add(types.InlineKeyboardButton(text=game['players'][ids]['name'], callback_data=str(game['players'][ids]['number'])))
        bot.send_message(game['players'][g]['id'], 'В кого ты хочешь выстрельнуть?', reply_markup=Keyboard)
    t=threading.Timer(endshoot, 20, args=[game])
        

        
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
    x=0
    for ids in games:
        if call.from_user.id in games[ids]['players']: 
            game=games[ids]
            x=1
    if x==1:
            for z in game:
                if game[z]['number']==int(call.data):
                    target=game[z]
            game[call.from_user.id]['text']=game[call.from_user.id]['name']+' стреляет в '+target['name']
            
        

def endshoot(game):
    text=''
    for ids in game:
        if game[ids]['text']!=None:
            text+=game[ids]['text']+'\n'
        else:
            text+=game[ids]['name']+' не стреляет\n'
    bot.send_message(game['id'], text)
        
        
def creategame(id):
    return {id:{
        'players':{},
        'id':id
    }
           }
        

def createuser(id, name, x):
    return{id:{
        'role':None,
        'name':name,
        'id':id,
        'number':x,
        'text':None
    }
          }
    
                      
                      
                      



if __name__ == '__main__':
  bot.polling(none_stop=True)



