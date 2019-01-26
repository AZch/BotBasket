import time
import traceback
from threading import Thread
from Games.sendGame import sendGame
from WorkWithTG import SendMsg
from ProcessGame import CheckGame


class Proc(Thread):


    def __init__(self, game, seasonYearStart, seasonYearEnd, procPool, lstGame, lstSendGame):
        Thread.__init__(self)
        self.game = game
        self.seasonStartYear = seasonYearStart
        self.seasonEndYear = seasonYearEnd
        self.lstGame = lstGame
        self.procPool = procPool
        self.lstSendGame = lstSendGame

    def run(self):
        self.startTime = time.time()
        try:
            if CheckGame.checkGame(self.game, self.seasonStartYear, self.seasonEndYear) and self.game.checkGame():
                self.game.isCheck = True
                print(self.game.report())
                #SendMsg.sendSimpleMsg(chatId=-1001497417479, text=self.game.report())  # -1001198541943
                #SendMsg.sendSimpleMsg(chatId=281265894, text=self.game.report())
                self.lstSendGame.append(sendGame(self.game.lstHome, self.game.lstAway, self.game.kf, self.game.elemFind))
                # try:
                #     self.lstGame.remove(self.game)
                # except:
                #     print('Ошибка:\n', traceback.format_exc())
            else:
                try:
                    self.lstGame.remove(self.game)
                except:
                    print('Ошибка:\n', traceback.format_exc())
        except:
            print('Ошибка123:\n', traceback.format_exc())
            pass
        self.procPool.returnProc(self)

    def clone(self, proc):
        return Proc(proc.game, proc.seasonStartYear, proc.seasonEndYear, proc.procPool, proc.lstGame, proc.lstSendGame)

    def setNewData(self, game, seasonYearStart, seasonYearEnd, procPool, lstGame, lstSendGame):
        self.game = game
        self.seasonStartYear = seasonYearStart
        self.seasonEndYear = seasonYearEnd
        self.procPool = procPool
        self.lstGame = lstGame
        self.lstSendGame = lstSendGame