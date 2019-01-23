import requests
from selenium import webdriver
import time
from LastGame import LastGame
from Game import Game
import traceback
from Constants import XPath
import ExecReq
import datetime
from threading import Thread

class Proc(Thread):


    def __init__(self, game, seasonYearStart, seasonYearEnd, procPool, lstGame):
        Thread.__init__(self)
        self.game = game
        self.seasonStartYear = seasonYearStart
        self.seasonEndYear = seasonYearEnd
        self.lstGame = lstGame
        self.procPool = procPool
        self.token = '760561600:AAEsDMxE0F8wSH3rZwkkuiDOqZOs_EBMiUM'
        self.URL = 'https://api.telegram.org/bot' + self.token + '/'

    def run(self):
        self.startTime = time.time()
        try:
            if self.checkGame(self.game, self.seasonStartYear, self.seasonEndYear) and self.game.checkGame():
                print(self.game.report())
                self.sendMsg(chatId=-1001497417479, text=self.game.report())  # -1001198541943
                self.sendMsg(chatId=281265894, text=self.game.report())
                try:
                    self.lstGame.remove(self.game)
                except:
                    print('Ошибка:\n', traceback.format_exc())
            else:
                self.game.setPrint()
                try:
                    self.lstGame.remove(self.game)
                except:
                    print('Ошибка:\n', traceback.format_exc())
        except:
            print('Ошибка:\n', traceback.format_exc())
            pass
        self.procPool.returnProc(self)

    def sendMsg(self, chatId, text="No"):
        url = self.URL + "sendMessage"
        answer = {"chat_id": chatId, "text": text}
        req = requests.post(url, json=answer)
        return req.json()

    def checkGame(self, game, seasonYearStart, seasonYearEnd):
        print(game.teams)
        driver = self.driverForPlayDay(game.dayFind, game.month)
        try:
            ExecReq.clickGetElem(driver, "//*[contains(text(), 'Agree')]")
            ExecReq.clickGetElem(driver, "//*[contains(text(), 'Scheduled')]")
            # elems = ExecReq.getElemsByXPath(XPath.allGame, driver)
            ExecReq.clickElem(self.getElemGame(driver, game.elemFind))
            driver.switch_to.window(driver.window_handles[1])
            game.currURL = driver.current_url

            ''' Получение коэффициента '''
            kf = ExecReq.getKF(driver)
            if kf == False or (kf[0] < 1.4 or kf[1] < 1.4):
                raise ValueError()
            elif kf[0] > kf[1]:
                isFirstTeam = False
            elif kf[1] > kf[0]:
                isFirstTeam = True
            else:
                isFirstTeam = True
                print("kf team equel")

            ''' Получить домашние игры '''
            ExecReq.clickGetElem(driver, XPath.clickH2H)
            ExecReq.clickGetElem(driver, XPath.clickHomeGame)
            while ExecReq.clickGetElem(driver, XPath.clickMoreHomeGame):
                pass
            elem = ExecReq.getElemsByXPath(XPath.homeGame, driver)
            home = self.parseLastCntWin(elems=elem, isFirstTeam=isFirstTeam, driver=driver,
                                   seasonYearStart=seasonYearStart, seasonYearEnd=seasonYearEnd)
            if home == False:
                raise ValueError()
            ''''''
            ''' Получить игры гостей '''
            print('away')
            ExecReq.clickGetElem(driver, XPath.clickAwayGame)
            while ExecReq.clickGetElem(driver, XPath.clickMoreAwayGame):
                pass

            elem = ExecReq.getElemsByXPath(XPath.awayGame, driver)
            away = self.parseLastCntWin(elems=elem, isFirstTeam=isFirstTeam, driver=driver,
                                   seasonYearStart=seasonYearStart, seasonYearEnd=seasonYearEnd)
            if away == False:
                raise ValueError()
            ''''''
            game.kf = kf
            game.lstHome = home
            game.lstAway = away
        except:
            print('Ошибка:\n', traceback.format_exc())
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            return False
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        return True

    def clone(self, proc):
        return Proc(proc.game, proc.seasonStartYear, proc.seasonEndYear, proc.procPool, proc.lstGame)

    def setNewData(self, game, seasonYearStart, seasonYearEnd, procPool, lstGame):
        self.game = game
        self.seasonStartYear = seasonYearStart
        self.seasonEndYear = seasonYearEnd
        self.procPool = procPool
        self.lstGame = lstGame

    def parseLastCntWin(self, elems, isFirstTeam, driver, seasonYearStart, seasonYearEnd):
        countElem = 0
        listRes = list()
        while 5 > len(listRes) and countElem < len(elems):
            yearGame = int("20" + elems[countElem].text.split()[0].split('.')[-1])
            if yearGame < seasonYearStart or yearGame > seasonYearEnd:
                break
            elems[countElem].click()
            driver.switch_to.window(driver.window_handles[2])
            print("----------------------------")
            kf = ExecReq.getKF(driver)
            if kf == False or (kf[0] < 1.3 or kf[1] < 1.3):
                countElem += 1
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                continue
            scoreFirst = ExecReq.getElemByXPath("//*[@class='odd']", driver)
            scoreSec = ExecReq.getElemByXPath("//*[@class='even']", driver)
            timeStart = time.time()
            while len(scoreFirst.text.split()) < 6 or len(scoreSec.text.split()) < 6:
                if time.time() - timeStart > 5:
                    break
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                elems[countElem].click()
                driver.switch_to.window(driver.window_handles[2])
                scoreFirst = ExecReq.getElemByXPath("//*[@class='odd']", driver)
                scoreSec = ExecReq.getElemByXPath("//*[@class='even']", driver)
            if (len(scoreFirst.text.split()) < 6 or len(scoreSec.text.split()) < 6):
                countElem += 1
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                continue
            lastGame = LastGame("", [scoreFirst.text, scoreSec.text])
            print("----------------------------")
            if lastGame.isCleanScore(isFirstTeam=isFirstTeam):
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                print("this game bad")
                return False
            listRes.append(lastGame)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            countElem += 1
        if len(listRes) < 5:
            print('to few game')
            return False
        driver.switch_to.window(driver.window_handles[1])
        return listRes

    def waitLoading(self, driver):
        while True:
            startTime = time.time()
            try:
                if ExecReq.getElemByXPath("//*[contains(text(), 'Loading')]", driver).text == '':
                    break
                if time.time() - startTime > 3:
                    break
            except:
                break

    def driverForPlayDay(self, day, month):
        driver = webdriver.Chrome("C:\\Users\\anton\\Desktop\\chromedriver.exe")
        driver.get('https://www.soccerstand.com/basketball/')
        while True:
            currDate = ExecReq.getElemByXPath("//*[@class='day today']", driver).text.split()[0]
            currDay = int(currDate.split('/')[0])
            currMonth = int(currDate.split('/')[1])
            if month < currMonth or day < currDay:
                ExecReq.clickGetElem(driver, "//*[@class='day yesterday']")
                self.waitLoading(driver)
            elif month > currMonth or day > currDay:
                ExecReq.clickGetElem(driver, "//*[@class='day tomorrow']")
                self.waitLoading(driver)
            else:
                break
        return driver

    def gameIdForPlayDay(self, driverGameDay, lstGame, dropLigue, day, month, prevDay, prevDayMonth):
        try:
            ExecReq.clickGetElem(driverGameDay, "//*[contains(text(), 'Agree')]")
            ExecReq.clickGetElem(driverGameDay, "//*[contains(text(), 'Scheduled')]")
            elemsLigue = ExecReq.getElemsByXPath("//table[@class='basketball']", driverGameDay)
            j = 0
            i = 0
            elems = ExecReq.getElemsByXPath(XPath.allGame, driverGameDay)
            while j < len(elemsLigue):
                ligueName = elemsLigue[j].text.split('\n')[1]
                print(ligueName)
                countGame = elemsLigue[j].text[len(elemsLigue[j].text.split('\n')[0] + "\n" + ligueName):].count(':')
                print(countGame)
                startI = i
                while i < startI + (countGame) * 2 and i < len(elems):
                    resCmd = elems[i].text + elems[i + 1].text
                    elemFind = elems[i].text.split('\n')[1]
                    resCmd = resCmd.translate({ord(c): None for c in '\n'})
                    if len(resCmd.split(' W-')) > 1:
                        i += 2
                        continue
                    timeGame = resCmd.split()[0].split(":")
                    timeGame = int(timeGame[0]) * 60 + int(timeGame[1])
                    if timeGame == 0:
                        timeGame = 24 * 60
                    print(resCmd)
                    isDrop = False
                    for oneDropLigue in dropLigue:
                        if oneDropLigue in ligueName:
                            i += 2
                            print('drop')
                            isDrop = True
                            break

                    if isDrop:
                        continue
                    if timeGame != 24 * 60:
                        # print("time 00:00")
                        newGame = Game(timeMin=timeGame, teams=resCmd, ligue=ligueName, day=day, month=month,
                                       idOnPage=i, elemFind=elemFind, dayFind=day)
                    else:
                        newGame = Game(timeMin=timeGame, teams=resCmd, ligue=ligueName, day=prevDay, month=prevDayMonth,
                                       idOnPage=i, elemFind=elemFind, dayFind=day)
                    lstGame.append(newGame)
                    i += 2
                j += 1
        except:
            print('Ошибка:\n', traceback.format_exc())
        driverGameDay.close()
        return lstGame

    def getElemGame(self, driver, gameBaseName):
        return ExecReq.getElemByXPath("//*[contains(text(), '" + gameBaseName + "')]", driver)