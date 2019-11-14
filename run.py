from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
from datetime import datetime
import random


@respond_to('今何時？')
def now(message):
    strftime = datetime.now().strftime(("%Y/%m/%d %H時%M分%S秒です！"))
    message.reply(strftime)


@respond_to('おみくじを引きたい！')
def omikuji(message):
    result = ['大吉', '吉', '中吉', '小吉', '末吉', '凶', '大凶']
    message.reply(random.choice(result))


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    print('slackbotが待っています、話しかけてね！')
    main()
