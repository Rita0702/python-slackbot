from datetime import datetime
import random
import csv

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

# オウム返し
# @respond_to('(.*)')
# def reply_message(message, arg):
#     message.reply(arg)