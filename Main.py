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
from proc import Proc
from ProcPool import ProcPool

def parseLastCntWin(elems, isFirstTeam, driver, seasonYearStart, seasonYearEnd):
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


token = '760561600:AAEsDMxE0F8wSH3rZwkkuiDOqZOs_EBMiUM'
URL = 'https://api.telegram.org/bot' + token + '/'

def sendMsg(chatId, text="No"):
    url = URL + "sendMessage"
    answer = {"chat_id": chatId, "text": text}
    req = requests.post(url, json=answer)
    return req.json()

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

def driverForPlayDay(day, month):
    driver = webdriver.Chrome("C:\\Users\\anton\\Desktop\\chromedriver.exe")
    driver.get('https://www.soccerstand.com/basketball/')
    while True:
        currDate = ExecReq.getElemByXPath("//*[@class='day today']", driver).text.split()[0]
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

def gameIdForPlayDay(driverGameDay, lstGame, dropLigue, day, month, prevDay, prevDayMonth):
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

def getElemGame(driver, gameBaseName):
    return ExecReq.getElemByXPath("//*[contains(text(), '" + gameBaseName + "')]", driver)

def checkGame(game, seasonYearStart, seasonYearEnd):
    print(game.teams)
    driver = driverForPlayDay(game.dayFind, game.month)
    try:
        ExecReq.clickGetElem(driver, "//*[contains(text(), 'Agree')]")
        ExecReq.clickGetElem(driver, "//*[contains(text(), 'Scheduled')]")
        #elems = ExecReq.getElemsByXPath(XPath.allGame, driver)
        ExecReq.clickElem(getElemGame(driver, game.elemFind))
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
        home = parseLastCntWin(elems=elem, isFirstTeam=isFirstTeam, driver=driver,
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
        away = parseLastCntWin(elems=elem, isFirstTeam=isFirstTeam, driver=driver,
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

def checkAndPrintGame(lstGame, game, seasonStart, seasonEnd):
    try:
        if checkGame(game, seasonStart, seasonEnd) and game.checkGame():
            print(game.report())
            sendMsg(chatId=-1001497417479, text=game.report()) #-1001198541943
            sendMsg(chatId=281265894, text=game.report())
            try:
                lstGame.remove(game)
            except:
                print('Ошибка:\n', traceback.format_exc())
        else:
            game.setPrint()
            try:
                lstGame.remove(game)
            except:
                print('Ошибка:\n', traceback.format_exc())
    except:
        print('Ошибка:\n', traceback.format_exc())
        pass

def startCheck(lstGame):
    dropLigue = ['USA', 'EURO', 'CANADA', 'ASIA', 'SWEDEN', 'JAPAN']
    date = datetime.datetime.now()
    driver = driverForPlayDay(date.day, date.month)
    datePrev = date + datetime.timedelta(days=-1)
    gameIdForPlayDay(driver, lstGame, dropLigue, date.day, date.month, datePrev.day, datePrev.month)
    # for game in lstGame:
    #     checkGame(game, date.year - 1, date.year + 1)
    goGameNextDay = True
    procPool = ProcPool(2)
    while True:
        if (not goGameNextDay and datetime.datetime.now().hour >= 2 and datetime.datetime.now().hour < 20):
            goGameNextDay = True
        if (goGameNextDay and datetime.datetime.now().hour >= 20):
            goGameNextDay = False
            date = datetime.datetime.now()
            dateNext = date + datetime.timedelta(days=1)
            driverNextDayGame = driverForPlayDay(dateNext.day, dateNext.month)
            ThreadPrse = Thread(target=gameIdForPlayDay, args=[driverNextDayGame, lstGame, dropLigue, dateNext.day, dateNext.month, date.day, date.month])
            ThreadPrse.start()
        for game in lstGame:
            if game.checkTime() and not game.isPrint():
                proc = procPool.getProc(game, date.year - 1, date.year + 1, lstGame)
                if proc != 'wait':
                    game.setPrint()
                    proc.start()
                    time.sleep(1)
                # ThreadCheckPrint = Thread(target=checkAndPrintGame, args=[lstGame, game, date.year - 1, date.year + 1])
                # ThreadCheckPrint.start()
                # time.sleep(40)
            elif game.checkTimeAfter():
                try:
                    lstGame.remove(game)
                except:
                    print('Ошибка:\n', traceback.format_exc())