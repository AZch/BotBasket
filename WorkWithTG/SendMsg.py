from WorkWithTG import myToken
import requests
from ProcessData import FindSort


def sendMsgInlineBtn(chatId, game, text="No"):
    url = myToken.URL + "sendMessage"
    answer = {"chat_id": chatId, "text": text,
              "reply_markup": {
                  "inline_keyboard": [
                      # [
                      #     {
                      #         "text": game.teamHome,
                      #         "callback_data": game.elemFind + "|Home"
                      #     }
                      #
                      # ],
                      # [
                      #     {
                      #         "text": game.teamAway,
                      #         "callback_data": game.elemFind + "|Away"
                      #     }
                      #
                      # ],
                      [
                          {
                              "text": "Fast ANALytics",
                              "callback_data": game.elemFind + "|Anal"
                          }

                      ],
                      [
                          {
                              "text": "SoCcErStAnD",
                              "url": game.currURL
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

# def anskek(id, data):
#     url = myToken.URL + "editMessageText?"
#     answer = {"chat_id": chatId, "message_id": text,
#               text
#               "reply_markup": {
#                   "inline_keyboard": [
#                       [
#                           {
#                               "text": game.teamHome,
#                               "callback_data": game.elemFind + "|Home"
#                           }
#
#                       ],
#                       [
#                           {
#                               "text": game.teamAway,
#                               "callback_data": game.elemFind + "|Away"
#                           }
#
#                       ],
#                       [
#                           {
#                               "text": "Fast ANALytics",
#                               "callback_data": game.elemFind + "|Anal"
#                           }
#
#                       ],
#                       [
#                           {
#                               "text": "SoCcErStAnD",
#                               "callback_data": game.elemFind + "|Link"
#                           }
#
#                       ]
#                   ]
#               }}
#     req = requests.post(url, json=answer)
#     return req.json()

def sendMsgAnswCallBack(id, data, lstSendGame):
    url = myToken.URL + "answerCallbackQuery?"
    # try:
    #     int(data)
    #     anskek(id, data)
    # except:
    #     pass
    if data.split('|')[1] == 'Link':
        answer = {
            "callback_query_id": id,
            "url": FindSort.findSendLink(data.split('|')[0], lstSendGame)
        }
    else:
        answer = {
                    "callback_query_id": id,
                    "text": FindSort.findSendGame(data, lstSendGame),
                    "show_alert": True
        }
    req = requests.post(url, json=answer)
    return req.json()