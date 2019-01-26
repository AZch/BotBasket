import time
from ProcessData import ExecReq
from Games.LastGame import LastGame
from selenium import webdriver
from Constants import XPath
import traceback
from Games.Game import Game
from WorkWithTG import myToken
from threading import Thread


def parseLastCntWin(elems, isFirstTeam, driver, seasonYearStart, seasonYearEnd):
    countElem = 0
    listRes = list()
    while 5 > len(listRes) and countElem < len(elems):
        yearGame = int("20" + elems[countElem].text.split()[0].split('.')[-1])
        if yearGame < seasonYearStart or yearGame > seasonYearEnd:
            break
        elems[countElem].click()
        driver.switch_to.window(driver.window_handles[2])
        startTime = time.time()
        while True:
            if time.time() - startTime > 90:
                break
            if ExecReq.getElemByXPath("//*[contains(text(), 'Match Summary')]", driver) == False:
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                elems[countElem].click()
                driver.switch_to.window(driver.window_handles[2])
            else:
                break
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

class makeDriver(Thread):
    def __init__(self):
        super().__init__()
        self.driver = None

    def run(self):
        self.driver = webdriver.Chrome(myToken.driverPath)
        self.driver.get('https://www.soccerstand.com/basketball/')

def getDriver():
    startTime = time.time()
    startAllTime = time.time()
    threadMakeDriver = makeDriver()
    threadMakeDriver.start()
    while True:
        if threadMakeDriver.driver != None:
            return threadMakeDriver.driver
        if time.time() - startTime > 240:
            threadMakeDriver = makeDriver()
            threadMakeDriver.start()
            startTime = time.time()

        if time.time() - startAllTime > 500:
            return threadMakeDriver.driver # скорее всего здесь None

def driverForPlayDay(day, month):
    driver = getDriver()
    while True:
        startTime = time.time()
        while True:
            if time.time() - startTime > 90:
                print ('tak i ne otrkirp')
                driver.close()
                return False
            try:
                currDate = ExecReq.getElemByXPath("//*[@class='day today']", driver).text.split()[0]
                break
            except:
                driver.get('https://www.soccerstand.com/basketball/')
                continue

        currDay = int(currDate.split('/')[0])
        currMonth = int(currDate.split('/')[1])
        if month < currMonth or day < currDay:
            ExecReq.clickGetElem(driver, "//*[@class='day yesterday']")
            waitLoading(driver)
        elif month > currMonth or day > currDay:
            ExecReq.clickGetElem(driver, "//*[@class='day tomorrow']")
            waitLoading(driver)
        else:
            break
    return driver

def waitLoading(driver):
    while True:
        startTime = time.time()
        try:
            if ExecReq.getElemByXPath("//*[contains(text(), 'Loading')]", driver).text == '':
                break
            if time.time() - startTime > 3:
                break
        except:
            break

def getElemGame(driver, gameBaseName):
    return ExecReq.getElemByXPath("//*[contains(text(), '" + gameBaseName + "')]", driver)

def gameIdForPlayDay(driverGameDay, lstGame, dropLigue, day, month, prevDay, prevDayMonth):
    try:
        ExecReq.clickGetElem(driverGameDay, "//*[contains(text(), 'Agree')]")
        ExecReq.clickGetElem(driverGameDay, "//*[contains(text(), 'Scheduled')]")
        elemsLigue = ExecReq.getElemsByXPath("//table[@class='basketball']", driverGameDay)
        j = 0
        i = 0
        elems = ExecReq.getElemsByXPath(XPath.allGame, driverGameDay)
        while j < len(elemsLigue):
            countLigue = 1
            ligueName = elemsLigue[j].text.split('\n')[1]
            countGame = elemsLigue[j].text[len(elemsLigue[j].text.split('\n')[0] + "\n" + ligueName):].count(':')
            try:
                int(ligueName.split(':')[0])
                ligueName = elemsLigue[j].text.split('\n')[0]
                countGame = elemsLigue[j].text[len(ligueName):].count(':')
                countLigue = 0
            except:
                pass
            print(ligueName)
            print(countGame)
            startI = i
            while i < startI + (countGame) * 2 and i < len(elems):
                resCmd = elems[i].text + elems[i + 1].text
                elemFind = elems[i + 1].text.split('\n')[0]
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
                    #print("time 00:00")
                    newGame = Game(timeMin=timeGame, teams=resCmd, ligue=ligueName, day=day, month=month, idOnPage=i, elemFind=elemFind, dayFind=day)
                else:
                    newGame = Game(timeMin=timeGame, teams=resCmd, ligue=ligueName, day=prevDay, month=prevDayMonth, idOnPage=i, elemFind=elemFind, dayFind=day)
                lstGame.append(newGame)
                i += 2
            j += 1
    except:
        print('Ошибка:\n', traceback.format_exc())
    driverGameDay.close()
    return lstGame
