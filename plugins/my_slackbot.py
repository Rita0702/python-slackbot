from datetime import datetime
import random
import csv
import requests
import json
import pya3rt
import slackbot_settings

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

@respond_to('^元気してる？')
def question_function1(message):
    message.react('smile')

@respond_to('アンケート (.*)')
def questionnaire(message, params):
    args = [row for row in csv.reader([params], delimiter=' ')][0]
    if len(args) < 3:
        message.reply('アンケート タイトル 質問 [質問 ...]')
        return

    EMOJIS = (
      'one',
      'two',
      'three',
      'four',
      'five',
    )

    title = args.pop(0)
    options = []
    for i, o in enumerate(args):
        options.append(':{}: {}'.format(EMOJIS[i], o))

    send_user = message.channel._client.users[message.body['user']]['name']
    post = {
        'pretext': '{}さんからアンケートがあります。'.format(send_user),
        'title': title,
        'author_name': send_user,
        'text': '\n'.join(options)
    }

    # 投稿内容をattachment形式で生成、送信
    ret = message._client.webapi.chat.post_message(
        message._body['channel'],
        username = message._client.login_data['self']['name'],
        as_user = True,
        attachments = [post]
    )

    # 送信した投稿に対してリアクションを付与
    ts = ret.body['ts']
    for i, _ in enumerate(options):
        message._client.webapi.reactions.add(
            name = EMOJIS[i],
            channel = message._body['channel'],
            timestamp = ts
        )

@respond_to('東京の天気は？')
def weather(message):
    city_id = '130010'
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=' + city_id
    data = requests.get(url).json()
    title = data["title"]
    forecasts_telop = data["forecasts"][0]['telop']
    text = data['description']['text']
    message.send(title)
    message.send('今日の天気は' + forecasts_telop + 'です！')
    message.send(text)
    message.send('お出かけするの？気をつけていってらっしゃい！')


@default_reply()
def send_message(message):
    apikey = slackbot_settings.A3RT_AP
    client = pya3rt.TalkClient(apikey)
    api_response = client.talk(message.body['text'])
    reply_message = api_response['results'][0]['reply']
    message.reply(reply_message)

# オウム返し
# @respond_to('(.*)')
# def reply_message(message, arg):
#     message.reply(arg)