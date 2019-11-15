from datetime import datetime
import random

from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
from slackbot.bot import default_reply 

@respond_to('今何時？')
def now(message):
    strftime = datetime.now().strftime(("%Y/%m/%d %H時%M分%S秒です！"))
    message.reply(strftime)

@respond_to('おみくじを引きたい！')
def omikuji(message):
    result = ['大吉', '吉', '中吉', '小吉', '末吉', '凶', '大凶']
    message.reply(random.choice(result))

@respond_to('メルカリ！')
def talk_function1(message):
    message.send('大好き') 
                                                         
@respond_to('メルカリに出品？')
def talk_function2(message):
    message.send('たくさんしてるよ')
                                                         
@respond_to('メルカリで購入は？')
def talk_function3(message):
    message.send('ほどほどにしてるかな')

# オウム返し
# @respond_to('(.*)')
# def reply_message(message, arg):
#     message.reply(arg)