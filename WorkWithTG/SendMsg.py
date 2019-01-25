from WorkWithTG import myToken
import requests
from ProcessData import FindSort


def sendMsgInlineBtn(chatId, game, text="No"):
    url = myToken.URL + "sendMessage"
    answer = {"chat_id": chatId, "text": text,
              "reply_markup": {
                  "inline_keyboard": [
                      [
                          {
                              "text": game.teamHome,
                              "callback_data": game.elemFind + "|Home"
                          }

                      ],
                      [
                          {
                              "text": game.teamAway,
                              "callback_data": game.elemFind + "|Away"
                          }

                      ]
                  ]
              }}
    req = requests.post(url, json=answer)
    return req.json()

def sendSimpleMsg(chatId, text="No"):
    url = myToken.URL + "sendMessage"
    answer = {"chat_id": chatId,
              "text": text}
    req = requests.post(url, json=answer)
    return req.json()

def sendMsgAnswCallBack(id, data, lstSendGame):
    url = myToken.URL + "answerCallbackQuery?"
    answer = {
                "callback_query_id": id,
                "text": FindSort.findSendGame(data, lstSendGame),
                "show_alert": True
    }
    req = requests.post(url, json=answer)
    return req.json()