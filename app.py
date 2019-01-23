from flask import Flask, request
import requests
from threading import Thread
import Main
from Game import Game
import myToken

lstGame = list()
mainFunc = Thread(target=Main.startCheck, args=[lstGame])
mainFunc.start()

token = myToken.token
URL = 'https://api.telegram.org/bot' + token + '/'

app = Flask(__name__)

def sendMsg(chatId, text="No"):
    url = URL + "sendMessage"
    answer = {"chat_id": chatId, "text": text}
    req = requests.post(url, json=answer)
    return req.json()

def getScoreAllGame():
    resStr = ""
    for game in lstGame:
        resStr += game.report() + "\n"
    return resStr

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    print('index')
    if request.method == 'POST':
        req = request.get_json()
        try:
            message = req['message']['text']
            if message == '/list':
                chatID = req['message']['from']['id']
                sendMsg(chatId=chatID, text=getScoreAllGame())
        except:
            print("bad")
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
