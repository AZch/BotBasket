import time
import traceback
import datetime
from threading import Thread
from ProcessGame.ProcPool import ProcPool
from ProcessData import ParseData
import ProcessGame.CheckGame
from WorkWithTG import SendMsg

def startCheck(lstGame, lstSendGame):
    dropLigue = ['USA', 'EURO', 'CANADA', 'ASIA', 'SWEDEN', 'JAPAN', 'Women', 'WOMEN']
    date = datetime.datetime.now()
    driver = ParseData.driverForPlayDay(date.day, date.month)
    datePrev = date + datetime.timedelta(days=-1)
    ParseData.gameIdForPlayDay(driver, lstGame, dropLigue, date.day, date.month, datePrev.day, datePrev.month)
    # for game in lstGame:
    #     checkGame(game, date.year - 1, date.year + 1)
    goGameNextDay = True
    checkSend = False
    procPool = ProcPool(2)
    while True:
        if (not goGameNextDay and datetime.datetime.now().hour >= 2 and datetime.datetime.now().hour < 20):
            goGameNextDay = True
        if (goGameNextDay and datetime.datetime.now().hour >= 20):
            goGameNextDay = False
            date = datetime.datetime.now()
            dateNext = date + datetime.timedelta(days=1)
            driverNextDayGame = ParseData.driverForPlayDay(dateNext.day, dateNext.month)
            ThreadPrse = Thread(target=ParseData.gameIdForPlayDay, args=[driverNextDayGame, lstGame, dropLigue, dateNext.day, dateNext.month, date.day, date.month])
            ThreadPrse.start()
        if datetime.datetime.now().minute < 5 and not checkSend:
            checkSend = True
            ThreadCheckSendGame = Thread(target=ProcessGame.CheckGame.checkSendGame, args=[lstSendGame])
            ThreadCheckSendGame.start()
        if datetime.datetime.now().minute > 5 and checkSend:
            checkSend = False


        for game in lstGame:
            if game.checkTime(timePrint=10) and game.isPrint() and game.isCheck:
                SendMsg.sendSimpleMsg(chatId=281265894, text=game.report())
                try:
                    lstGame.remove(game)
                except:
                    print('Ошибка:\n', traceback.format_exc())
            if game.checkTime() and not game.isPrint():
                if not game.isPrint():
                    proc = procPool.getProc(game, date.year - 1, date.year + 1, lstGame, lstSendGame)
                    if proc != 'wait':
                        game.setPrint()
                        proc.start()
                        time.sleep(5)
                # ThreadCheckPrint = Thread(target=checkAndPrintGame, args=[lstGame, game, date.year - 1, date.year + 1])
                # ThreadCheckPrint.start()
                # time.sleep(40)
            elif game.checkTimeAfter():
                try:
                    lstGame.remove(game)
                except:
                    print('Ошибка:\n', traceback.format_exc())