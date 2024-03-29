#!/usr/bin/python3
import traceback
from flask import Flask, request
from threading import Thread
import StartParseFind
from WorkWithTG import SendMsg
from ProcessData import FindSort
import telebot
import cherrypy
from WorkWithTG import myToken

lstGame = list()
lstSendGame = list()
mainFunc = Thread(target=StartParseFind.startCheck, args=[lstGame, lstSendGame])
mainFunc.start()

WEBHOOK_HOST = '128.199.38.189'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '128.199.38.189'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (myToken.token)

bot = telebot.TeleBot(myToken.token)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                       'content-type' in cherrypy.request.headers and \
                       cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)

            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

@bot.message_handler(commands=["iswork"])
def sendWorkStatus(message):
    SendMsg.sendSimpleMsg(chatId=message.chat.id, text='yes, count game: ' + str(len(lstGame)))

@bot.message_handler(commands=["list"])
def sendLstGame(message):
    SendMsg.sendSimpleMsg(chatId=message.chat.id, text=FindSort.getScoreAllGame(lstGame))

@bot.callback_query_handler(func=lambda call: True)
def callbackBtn(call):
    if call.message:
        SendMsg.sendMsgAnswCallBack(call.id, call.data, lstSendGame)

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, 
                         certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})



'''
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    print('index')
    if request.method == 'POST':
        req = request.get_json()
        try:
            SendMsg.sendMsgAnswCallBack(req['callback_query']['id'], req['callback_query']['data'], lstSendGame)
        except:
            try:
                message = req['message']['text']
                if message == '/list':
                    chatID = req['message']['from']['id']
                    SendMsg.sendSimpleMsg(chatId=chatID, text=FindSort.getScoreAllGame(lstGame))
                if message == '/iswork':
                    chatID = req['message']['from']['id']
                    SendMsg.sendSimpleMsg(chatId=chatID, text='yes, count game: ' + str(len(lstGame)))
            except:
                print('Ошибка:\n', traceback.format_exc())
                print("bad")
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
'''
