import traceback
from flask import Flask, request
from threading import Thread
import StartParseFind
from WorkWithTG import SendMsg
from ProcessData import FindSort

lstGame = list()
lstSendGame = list()
mainFunc = Thread(target=StartParseFind.startCheck, args=[lstGame, lstSendGame])
mainFunc.start()

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
